""""""
import fnmatch
import os

import requests

NEWT_BASE_URL = 'https://newt.nersc.gov/newt'
MACHINE = 'cori'


class NerscInterface:
    def __init__(self, login_notebook='nersc_login.ipynb'):
        """"""
        self._login_notebook = login_notebook  # for error messages (only)
        self._newt_sessionid = None
        self._requests_session = requests.Session()


    def get_job_info(self, job_id, machine=MACHINE, verbose=False):
        assert self._newt_sessionid is not None

        if verbose:
            print('sending command...')

        url = '{}/queue/{}/{}/sacct'.format(NEWT_BASE_URL, machine, job_id)
        r = self._requests_session.get(url)
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

        data = {
          'executable': 'echo $SCRATCH',
          'loginenv': 'true'
        }
        url = '%s/command/%s' % (NEWT_BASE_URL, machine)
        r = self._requests_session.post(url, data=data)
        r.raise_for_status()

        js = r.json()
        scratch_folder = js.get('output')
        return scratch_folder


    def list_folder(self, nersc_folder, glob_pattern=None, machine=MACHINE):
        """Returns a GENERATOR with contents of a folder.

        Args:
            pattern: string for matching filename, e.g., '*.xml'
        """
        url = '%s/file/%s/%s' % (NEWT_BASE_URL, machine, nersc_folder)
        r = self._requests_session.get(url)
        r.raise_for_status()

        paths = r.json()

        for path in paths:
            if glob_pattern is not None and \
                    not fnmatch.fnmatch(path['name'], glob_pattern):
                continue

            del path['perms']
            del path['hardlinks']

            path['size'] = int(path['size'])
            yield path


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

        url = '{}/login/'.format(NEWT_BASE_URL)
        cookies = dict(newt_sessionid=newt_sessionid)
        r = requests.get(url, cookies=cookies)
        r.raise_for_status()

        js = r.json()
        # print('login reply', js)
        # Example reply:
        # {'username': 'johnt', 'session_lifetime': 976394, 'auth': True, 'newt_sessionid': '0fc3f5310b54310f08bdcbf690d5c255'}
        if 'auth' not in js or not js['auth']:
            print('Reply:', js)
            raise Exception('User not logged in => use {}'.format(self._login_notebook))

        if hasattr(js, 'session_lifetime') and js['session_lifetime'] < 300:
            print('Reply:', js)
            template = 'Session lifetime about to expire ({} sec) => use {}'
            raise Exception(template.format(js['session_lifetime'], self._login_notebook))

        self._newt_sessionid = newt_sessionid
        self._requests_session.cookies.set('newt_sessionid', self._newt_sessionid)
        return 'OK'


    def make_folder(self, nersc_folder, machine=MACHINE):
        assert self._newt_sessionid is not None
        print('sending command...')

        data = {
          'executable': 'mkdir -p {}'.format(nersc_folder),
          'loginenv': 'true'
        }
        url = '%s/command/%s' % (NEWT_BASE_URL, machine)
        r = self._requests_session.post(url, data=data)
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
        r = self._requests_session.post(url, files={'file': (job_filename, slurm_script)})
        r.raise_for_status()

        print('submitting job...')
        url = '{}/queue/{}'.format(NEWT_BASE_URL, machine)
        data = {
            'jobfile': '{}/{}'.format(nersc_folder, job_filename)
        }
        r = self._requests_session.post(url, data=data)
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
            r = self._requests_session.post(url, files={'file': (filename, f)})
            r.raise_for_status()
        return 'OK'


if __name__ == '__main__':
    nersc = NerscInterface()
    nersc.login()
    sf = nersc.get_scratch_folder()
    print('$SCRATCH folder:', sf)
