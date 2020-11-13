from ipyfilechooser import FileChooser
import ipywidgets as widgets
import os
import requests
import threading

from . import ats_runner


def _make_int_slider(value, min, max, title):
    return widgets.IntSlider(
        value=value,
        min=min,
        max=max,
        step=1,
        description=title,
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='d'
    )


class RepeatTimer(threading.Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            try:
                self.function(*self.args, **self.kwargs)
            except requests.exceptions.HTTPError:
                pass


class ATSWidget(object):
    """An extension of ATSRunner for controlling via widgets in a Jupyter
    notebook.

    """
    def __init__(self,):
        working_dir = os.getcwd()

        self.scratch_folder = widgets.Text(
            value='demo',
            placeholder='Name of scratch folder on NERSC',
            description='Scratch folder:',
            disabled=False
        )


        self.nodes_slider = _make_int_slider(1, 1, 32, '# Nodes:')
        self.cores_slider = _make_int_slider(1, 1, 32, '# Cores:')
        self.timeout_field = widgets.BoundedIntText(
            value=5,
            min=0,
            max=100,
            step=1,
            description='Timeout (min):',
            disabled=False
        )
        # self.verbosity_checkbox = widgets.Checkbox(
        #     value=False,
        #     description='Verbose:',
        #     disabled=False,
        #     indent=False
        # )

        self.xml_selector = FileChooser(working_dir,
                                        use_dir_icons=True,
                                        title="XML File")
        self.data_selector = FileChooser(working_dir,
                                         show_only_dirs=True,
                                         use_dir_icons=True,
                                         title="Data Directory")

        self.submit_button = widgets.Button(
            description='Submit',
            disabled=False,
            button_style='success', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Submit job to NERSX',
            icon='upload', # (FontAwesome names without the `fa-` prefix)
        )
        self.submit_button.on_click(lambda *args: self._submit_callback())

        self.progress_widget = widgets.FloatProgress(value=0.0, min=0.0, max=5.0)

        self.output = widgets.Output(layout={'border': '5px solid black',
                                             'width': '100%',
                                             'height': '250px',
                                             'overflow_y':'auto',
                                             })

        self.download_button = widgets.Button(
            description='Download',
            disabled=True,
            button_style='info', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Download results',
            icon='download', # (FontAwesome names without the `fa-` prefix)
        )

        def _download_callback(*absrgs):
            self.local_folder = self.runner.download()

        self.download_button.on_click(_download_callback)

        layout = widgets.Layout(display='align-self',
                                border='solid 1px',
                                width='100%',
                                max_height='750px',)

        self.ui = widgets.HBox([
            widgets.VBox([
                self.scratch_folder,
                self.nodes_slider,
                self.cores_slider,
                widgets.HBox([self.timeout_field, ]),#self.verbosity_checkbox]),
                self.xml_selector,
                self.data_selector,
                widgets.HBox([self.submit_button, self.download_button,]),
            ]),
            widgets.VBox([self.output, self.progress_widget], layout=layout)
        ], layout=layout)


    def _log(self, msg):
        return self.output.append_stdout(msg + '\n')

    def _submit_callback(self):
        if self.xml_selector.selected_path is None:
            self._log("Please select an XML file.")
            return
        # Run the job
        self.submit_button.disabled = True
        logger = lambda msg: self._log(msg)
        self.runner = ats_runner.ATSRunner(
            scratch_folder=self.scratch_folder.value,
            local_xml=self.xml_selector.selected,
            data=self.data_selector.selected_path,
            timeout_min=self.timeout_field.value,
            nodes=self.nodes_slider.value,
            cores_per_node=self.cores_slider.value,
            # verbose=self.verbosity_checkbox.value,
            logger=logger,
        )

        self.runner.run()
        # Check that the submission was successful
        if self.runner._submission['status'] != 'OK':
            self._log("Submission error: {}".format(self.runner._submission))
            self.submit_button.disabled = False
            return
        else:
            self._log("Submission success.")
            self.submit_button.disabled = True

        # Update the progress widget
        self.progress_widget.description = 'Submitted'
        self.progress_widget.value = 1.0
        # Add callback to periodically check status and update progress bar

        self._status_timer = RepeatTimer(1, lambda: self._check_status())
        self._status_timer.start()

    def _check_status(self):
        status = self.runner.check_status()
        label = self.runner._nersc.job_state_label(status)
        msg = '{} ({})'.format(status, label)
        self.progress_widget.description = msg
        v = dict(
            PD=2, #"Pending",
            R=3, #"Running",
            CG=4, #"Completing",
            CD=5 #"Completed",
        )
        try:
            self.progress_widget.value = v[status]
        except KeyError:
            pass
        if status in ['CD', 'F', 'RNF', 'OOM', 'TO']:
            self._status_timer.cancel()
            self.runner._nersc._log("Job finished: {}".format(label))
            self.download_button.disabled = False
        return msg

    def __del__(self):
        if hasattr(self, '_status_timer'):
            self._status_timer.cancel()
