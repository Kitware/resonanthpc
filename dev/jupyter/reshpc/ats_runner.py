import datetime
import os
import shutil
import tarfile

from . import nersc_interface

class ATSRunner(object):
    """A helper class to run ATS simulations at NERSC

    Parameters
    ----------
    scratch_folder : str
        The name of the scratch folder to run this simulation. This will be
        appended with the datetime of creation of this object.

    local_xml : str
        The path to the XML input deck for the simulation on the local machine
        (wherever this Python is running).

    resources : tuple(str)
        An iterable of str paths of additional resources to add to the scratch
        folder in a subfolder ``data`` adjacent to the XML file. Be sure to
        reference any of these resources in your XML input deck as `./data/*`.

    """
    ATS_EXECUTABLE = '/project/projectdirs/m2398/ideas/ats/install/cori/ats-0.88-basic/RelWithDebInfo/PrgEnv-gnu-6.0.5/bin/ats'

    def __init__(self, scratch_folder, local_xml, data=None, timeout_min=5,
                 nodes=1, cores_per_node=1, verbose=False, logger=None):
        self._nersc = nersc_interface.NerscInterface(verbose=verbose, logger=logger)
        # Use datetime of creation of this object for it's working dir
        self._datetime_code = datetime.datetime.now().strftime('%y%m%d-%H%M')
        # Check given files
        if not os.path.isfile(local_xml):
            raise FileNotFoundError("The local XML file does not exist: `{}`".format(local_xml))
        if data is not None and not os.path.isdir(data):
            raise FileNotFoundError("The data directory does not exist: `{}`".format(data))
        # Local stuff
        self.local_xml = local_xml
        self.data_dir = data
        # Simulation params
        self.timeout_min = timeout_min
        self.nodes = nodes
        self.cores_per_node = cores_per_node
        # Create working folder on NERSC
        self.scratch_folder = scratch_folder
        self._setup()

    def _setup(self):
        # Generate path on Cori $SCRATCH folder
        scratch_folder = self._nersc.get_scratch_folder()
        self.nersc_folder = '{}/{}/{}'.format(scratch_folder, self.scratch_folder, self._datetime_code)
        self._nersc.make_folder(self.nersc_folder)
        self.nersc_folder_data = os.path.join(self.nersc_folder, 'data')
        self._nersc.make_folder(self.nersc_folder_data)

    def _generate_slurm_script(self):
        if not hasattr(self, '_xml_file'):
            raise RuntimeError("Must upload assets before submitting job.")

        slurm_commands = [
            '#!/bin/bash',
            '#SBATCH --account=m2398',
            '#SBATCH --chdir={}'.format(self.nersc_folder),
            '#SBATCH --partition=debug',
            '#SBATCH --time=0:{}:0'.format(self.timeout_min),
            '#SBATCH --nodes={}'.format(self.nodes),
            '#SBATCH --tasks-per-node={}'.format(self.cores_per_node),
            '#SBATCH --constraint=haswell',
            'ulimit -s unlimited',
            'srun {} --xml_file={}'.format(self.ATS_EXECUTABLE, self._xml_file),
            ''
        ]

        return '\n'.join(slurm_commands)

    def _upload(self):
        self._xml_file = os.path.basename(self.local_xml)
        self._nersc.upload_file(self.local_xml, self.nersc_folder)
        if self.data_dir is not None:
            self._nersc.upload_folder(os.path.abspath(self.data_dir), self.nersc_folder_data)

    def _submit(self):
        slurm_string = self._generate_slurm_script()
        self._submission = self._nersc.submit_job(slurm_string, self.nersc_folder)
        return self._submission

    def run(self):
        self._upload()
        self._submit()

    def check_status(self):
        """Check status of job.

        All of the Slurm job state codes are listed at https://slurm.schedmd.com/squeue.html#lbAG

        If the job successfully runs, the Job State will typically traverse
        these values:

        | Job State Code | Description |
        |----------------|-------------|
        | PD             | pending     |
        | R              | running     |
        | CG             | completing  |
        | CD             | completed   |

        If problems occur, the most relevant Job State codes are:

        | Job State Code | Description   |
        |----------------|---------------|
        | F              | failed        |
        | RNF            | node failed   |
        | OOM            | out of memory |
        | TO             | timeout       |

        """
        job_id = self._submission.get('jobid')
        if job_id:
            info = self._nersc.get_job_info(job_id)
            state = info.get('status')
            return state
        else:
            return "job has not been submitted."

    def list_folder(self, sub='', glob_pattern='*.*'):
        """List contents of working directory on NERSC."""
        contents = {}
        for item in self._nersc.list_folder(self.nersc_folder + sub, glob_pattern=glob_pattern):
            name = item.get('name')
            size = int(item.get('size', 0))
            contents[name] = '{:8}'.format(size)
        return contents

    def download(self, glob_pattern='*.*'):
        """Tar up and download from the scratch folder."""
        tarfile_name = 'contents.tgz'
        nersc_tarfile = '{}/reshpc/{}'.format(self._nersc.get_scratch_folder(), tarfile_name)
        self._nersc.make_tgzfile(self.nersc_folder, glob_pattern=glob_pattern, tarfile=nersc_tarfile)
        # Create local data folder and download tar file
        local_folder = os.path.expanduser('~/.reshpc/data/{}'.format(self._datetime_code))
        if os.path.exists(local_folder):
            shutil.rmtree(local_folder)
        os.makedirs(local_folder)
        self._nersc.download_file(nersc_tarfile, local_folder)
        # Expand local archive
        local_tarfile = os.path.join(local_folder, tarfile_name)
        tar = tarfile.open(local_tarfile)
        tar.extractall(local_folder)
        tar.close()
        self._nersc._log(local_folder)
        return local_folder
