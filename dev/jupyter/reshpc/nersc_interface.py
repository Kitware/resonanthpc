""""""
import fnmatch
import os

import requests

from .assets import NEWT_BASE_URL, MACHINE, REQUESTS_SESSION


class NerscInterface:
    def __init__(self, login_notebook="nersc_login.ipynb"):
        """"""
        self._login_notebook = login_notebook  # for error messages (only)
        self._requests_session = REQUESTS_SESSION
        self._newt_sessionid = REQUESTS_SESSION.cookies.get("newt_sessionid")

    def download_file(self, nersc_file, local_folder, machine=MACHINE):
        assert self._newt_sessionid is not None
        print("sending command...")

        url = "%s/file/%s/%s" % (NEWT_BASE_URL, machine, nersc_file)
        params = {"view": "read"}

        filename = os.path.basename(nersc_file)
        local_file = os.path.join(local_folder, filename)

        # Per https://stackoverflow.com/a/16696317
        with self._requests_session.get(url, params=params, stream=True) as r:
            r.raise_for_status()
            with open(local_file, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return "OK"

    def file_exists(self, nersc_file, machine=MACHINE):
        """Returns boolean indicating whether or not file exists at the path"""
        print("sending command...")

        url = "%s/file/%s/%s" % (NEWT_BASE_URL, machine, nersc_file)
        r = self._requests_session.get(url)
        return r.status_code == requests.codes.ok

    def get_job_info(self, job_id, machine=MACHINE, verbose=False):
        assert self._newt_sessionid is not None

        if verbose:
            print("sending command...")

        url = "{}/queue/{}/{}/sacct".format(NEWT_BASE_URL, machine, job_id)
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
        print("sending command...")

        data = {"executable": "echo $SCRATCH", "loginenv": "true"}
        url = "%s/command/%s" % (NEWT_BASE_URL, machine)
        r = self._requests_session.post(url, data=data)
        r.raise_for_status()

        js = r.json()
        scratch_folder = js.get("output")
        return scratch_folder

    def job_state_label(self, state):
        """Returns the text associated with the most common job state codes.

        Copied from https://slurm.schedmd.com/squeue.html#lbAG
        """
        lookup = dict(
            CD="Completed",
            CG="Completing",
            F="Failed",
            NF="Node Fail",
            OOM="Out Of Memory",
            PD="Pending",
            R="Running",
            TO="Time Out",
        )
        return lookup.get(state, "Unrecognized")

    def list_folder(self, nersc_folder, glob_pattern=None, machine=MACHINE):
        """Returns a GENERATOR with contents of a folder.

        Args:
            pattern: string for matching filename, e.g., '*.xml'
        """
        assert self._newt_sessionid is not None
        print("sending command...")

        url = "%s/file/%s/%s" % (NEWT_BASE_URL, machine, nersc_folder)
        r = self._requests_session.get(url)
        r.raise_for_status()

        paths = r.json()

        for path in paths:
            if glob_pattern is not None and not fnmatch.fnmatch(
                path["name"], glob_pattern
            ):
                continue

            del path["perms"]
            del path["hardlinks"]

            path["size"] = int(path["size"])
            yield path

    def make_folder(self, nersc_folder, machine=MACHINE):
        assert self._newt_sessionid is not None
        print("sending command...")

        data = {"executable": "mkdir -p {}".format(nersc_folder), "loginenv": "true"}
        url = "%s/command/%s" % (NEWT_BASE_URL, machine)
        r = self._requests_session.post(url, data=data)
        r.raise_for_status()
        return "OK"

    def make_tgzfile(self, nersc_folder, tarfile, glob_pattern="*.*", machine=MACHINE):
        """"""
        assert self._newt_sessionid is not None
        print("sending command...")

        cmd = (
            "rm -f {tarfile} && cd {nersc_folder} && tar -czf {tarfile} {files}".format(
                tarfile=tarfile, nersc_folder=nersc_folder, files=glob_pattern
            )
        )
        # print('cmb:', cmd)
        data = {"executable": cmd, "loginenv": "true"}
        url = "%s/command/%s" % (NEWT_BASE_URL, machine)
        r = self._requests_session.post(url, data=data)
        r.raise_for_status()
        return "OK"

    def submit_job(
        self, slurm_script, nersc_folder, job_filename="job.sbatch", machine=MACHINE
    ):
        """Submits job to queue.


        Uploads slurm_script as file to nersc_folder.
        Returns dict with ['status', 'error', 'jobid'] keys or raises exception.
        """
        assert self._newt_sessionid is not None
        print("uploading slurm script...")

        url = "{}/file/{}{}".format(NEWT_BASE_URL, machine, nersc_folder)
        r = self._requests_session.post(
            url, files={"file": (job_filename, slurm_script)}
        )
        r.raise_for_status()

        print("submitting job...")
        url = "{}/queue/{}".format(NEWT_BASE_URL, machine)
        data = {"jobfile": "{}/{}".format(nersc_folder, job_filename)}
        r = self._requests_session.post(url, data=data)
        r.raise_for_status()

        js = r.json()
        return js

    def upload_file(self, local_path, nersc_folder, machine=MACHINE):
        """"""
        assert self._newt_sessionid is not None
        assert os.path.exists(local_path), "Local file not found: {}".format(local_path)
        print("sending command...")

        url = "{}/file/{}{}".format(NEWT_BASE_URL, machine, nersc_folder)
        cookies = dict(newt_sessionid=self._newt_sessionid)
        filename = os.path.basename(local_path)
        with open(local_path, "rb") as f:
            # Found the syntax for "files" from cumulus.transport.newt:
            r = self._requests_session.post(url, files={"file": (filename, f)})
            r.raise_for_status()
        return "OK"


if __name__ == "__main__":
    nersc = NerscInterface()
    nersc.login()
    sf = nersc.get_scratch_folder()
    print("$SCRATCH folder:", sf)
