""""""
import os

import requests

NEWT_BASE_URL = 'https://newt.nersc.gov/newt'
MACHINE = 'cori'


class NerscInterface:
    def __init__(self, login_notebook='nersc_login.ipynb'):
        """"""
        self._login_notebook = login_notebook  # for error messages (only)
        self._newt_sessionid = None


    def get_job_info(self, job_id, machine=MACHINE, verbose=False):
        assert self._newt_sessionid is not None

        if verbose:
            print('sending command...')

        cookies = dict(newt_sessionid=self._newt_sessionid)
        url = '{}/queue/{}/{}/sacct'.format(NEWT_BASE_URL, machine, job_id)
        r = requests.get(url, cookies=cookies)
        r.raise_for_status()

        js = r.json()
        return js


    def get_scratch_folder(self, machine=MACHINE):
        """Requests path to the user'S $SCRATCH directory on the NERSC machine

        Since the scratch directory is specific to each user,
        this method only returns a valid result after successful login().
        """
        assert self._newt_sessionid is not None
        print('sending command...')

        cookies = dict(newt_sessionid=self._newt_sessionid)
        data = {
          'executable': 'echo $SCRATCH',
          'loginenv': 'true'
        }
        url = '%s/command/%s' % (NEWT_BASE_URL, machine)
        r = requests.post(url, cookies=cookies, data=data)
        r.raise_for_status()

        js = r.json()
        scratch_folder = js.get('output')
        return scratch_folder


    def login(self, file='~/.newt_sessionid', newt_sessionid=None):
        """"""
        if newt_sessionid is None:
            path = os.path.expanduser(file)
            if not os.path.exists(path):
                template = 'File {} missing => use {}'
                raise RuntimeError(template.format(file, self._login_notebook))

            with open(path) as f:
                newt_sessionid = f.read().strip()
        assert newt_sessionid is not None
        print('sending command...')

        cookies = dict(newt_sessionid=newt_sessionid)
        url = '{}/login/'.format(NEWT_BASE_URL)
        r = requests.get(url, cookies=cookies)
        r.raise_for_status()

        js = r.json()
        # print('login reply', js)
        # Example reply:
        # {'username': 'johnt', 'session_lifetime': 976394, 'auth': True, 'newt_sessionid': '0fc3f5310b54310f08bdcbf690d5c255'}
        if 'auth' not in js or not js['auth']:
            raise Exception('User not logged in => use {}'.format(self._login_notebook))

        if hasattr(js, 'session_lifetime') and js['session_lifetime'] < 300:
            template = 'Session lifetime about to expire ({} sec) => use {}'
            raise Exception(template.format(js['session_lifetime'], self._login_notebook))

        self._newt_sessionid = newt_sessionid
        return 'OK'


    def make_folder(self, nersc_folder, machine=MACHINE):
        assert self._newt_sessionid is not None
        print('sending command...')

        cookies = dict(newt_sessionid=self._newt_sessionid)
        data = {
          'executable': 'mkdir -p {}'.format(nersc_folder),
          'loginenv': 'true'
        }
        url = '%s/command/%s' % (NEWT_BASE_URL, machine)
        r = requests.post(url, cookies=cookies, data=data)
        r.raise_for_status()
        return 'OK'


    def submit_job(self, slurm_script, nersc_folder, job_filename='job.sbatch', machine=MACHINE):
        """Submits job to queue.


        Uploads slurm_script as file to nersc_folder.
        Returns dict with ['status', 'error', 'jobid'] keys or raises exception.
        """
        assert self._newt_sessionid is not None

        print('uploading slurm script...')
        url = '{}/file/{}{}'.format(NEWT_BASE_URL, machine, nersc_folder)
        cookies = dict(newt_sessionid=self._newt_sessionid)
        r = requests.post(url, cookies=cookies, files={'file': (job_filename, slurm_script)})
        r.raise_for_status()

        print('submitting job...')
        url = '{}/queue/{}'.format(NEWT_BASE_URL, machine)
        data = {
            'jobfile': '{}/{}'.format(nersc_folder, job_filename)
        }
        r = requests.post(url, cookies=cookies, data=data)
        r.raise_for_status()

        js = r.json()
        return js


    def upload_file(self, local_path, nersc_folder, machine=MACHINE):
        """"""
        assert self._newt_sessionid is not None
        assert os.path.exists(local_path), 'Local file not found: {}'.format(local_path)
        print('sending command...')

        url = '{}/file/{}{}'.format(NEWT_BASE_URL, machine, nersc_folder)
        cookies = dict(newt_sessionid=self._newt_sessionid)
        filename = os.path.basename(local_path)
        with open(local_path, 'rb') as f:
            # Found the syntax for "files" from cumulus.transport.newt:
            r = requests.post(url, cookies=cookies, files={'file': (filename, f)})
            r.raise_for_status()
        return 'OK'


if __name__ == '__main__':
    nersc = NerscInterface()
    nersc.login()
    sf = nersc.get_scratch_folder()
    print('$SCRATCH folder:', sf)
