from fractions import Fraction
import logging
#import logging.handlers

from tardis.tardis_portal.models import Schema, DatafileParameterSet
from tardis.tardis_portal.models import ParameterName, DatafileParameter
import subprocess
import tempfile
import base64
import os
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
import numpy as np
import matplotlib
#http://matplotlib.org/faq/usage_faq.html#what-is-a-backend
matplotlib.use('AGG')
#perhaps need to install ---yum install agg

import mne
from mne.fiff import Raw
from mne.datasets import sample
from mne import fiff

logger = logging.getLogger(__name__)

"""
LOG_FILENAME = '/opt/mytardis/current/MNE.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO)
"""
class MNEImageFilter(object):


    """If a white list is specified then it takes precidence and all
    other tags will be ignored.

    :param name: the short name of the schema.
    :type name: string
    :param schema: the name of the schema to load the EXIF data into.
    :type schema: string
    :param tagsToFind: a list of the tags to include.
    :type tagsToFind: list of strings
    :param tagsToExclude: a list of the tags to exclude.
    :type tagsToExclude: list of strings
    """
    def __init__(self, name, schema, tagsToFind=[], tagsToExclude=[]):
        self.name = name
        self.schema = schema
        self.tagsToFind = tagsToFind
        self.tagsToExclude = tagsToExclude
	logger.error('MNE-init()')
	logger.debug('initialising MNEImageFilter')

    def __call__(self, sender, **kwargs):
        """post save callback entry point.
        logger.debug('MNE-init()')
        :param sender: The model class.
        :param instance: The actual instance being saved.
        :param created: A boolean; True if a new record was created.
        :type created: bool
        """
	logger.error('MNE-call()')
	instance = kwargs.get('instance')

        schema = self.getSchema()

        filepath = instance.get_absolute_filepath()

        raw_fname = filepath

        """:only process MNE fif files"""
        if not filepath.endswith('.fif'):
            return None

        try:

            logger.error('MNE-fif image found')	

            #handle MNE files
            #get raw data
            raw = Raw(raw_fname)
	    

            metadata_dump = dict()

            ###############################################################################
            # explore some nitime timeseries features
            logger.error('step 1')	

            # get start
            #metadata_dump['start'] = raw.t0

            logger.error('step 1.0')

            # get sampling frequnecy
            metadata_dump['sampling_frequency'] = raw.info['sfreq']

            logger.error('step 1.1')

            # get bad channel lists
            metadata_dump['bads'] = raw.info['bads']

            logger.error('step 1.2')

            # get projects
            metadata_dump['projects'] = raw.info['projs']

            # get measure date
            metadata_dump['measure_date'] = raw.info['meas_date']

            # get measure id
            metadata_dump['measure_id'] = raw.info['meas_id']

            # get file id logger.error('image_information ' + raw.info['file_id'])
            #metadata_dump['image_information'] = 'Some fixed value'
	    #metadata_dump['image_information'] = raw.info['comps']
	    logger.error('step 1.2.1')
            metadata_dump['experimenter'] = raw.info['experimenter']
            logger.error(metadata_dump['experimenter'])
	    logger.error('step 1.2.2')
            metadata_dump['description'] = raw.info['description']
            logger.error(metadata_dump['description'])
            #logger.error('step 1.2.3')
            #metadata_dump['proj_id'] = raw.info['proj_id']
	    #logger.error(metadata_dump['proj_id'])
            logger.error('step 1.2.3')
            metadata_dump['proj_name'] = raw.info['proj_name']
	    logger.error(metadata_dump['proj_name'])
	    #logger.error('step 1.2.5')
            #metadata_dump['chs'] = raw.info['chs']
	    #logger.error(metadata_dump['chs'])
	    #logger.error('step 1.2.6')
            #metadata_dump['secs'] = raw.info['meas_id']['secs']
	    #logger.error('step 1.2.7')
            #metadata_dump['usecs'] = raw.info['meas_id']['usecs']
	    #logger.error('step 1.2.8')
            #metadata_dump['comps'] = raw.info['comps']
	    #logger.error(metadata_dump['comps'])
	    #logger.error('step 1.2.9')
            #metadata_dump['acq_pars'] = raw.info['acq_pars']
	    #logger.error(metadata_dump['acq_pars'])
	    logger.error('step 1.2.4')
            metadata_dump['acq_stim'] = raw.info['acq_stim']
	    logger.error(metadata_dump['acq_stim'])
	    #logger.error('step 1.2.11')
            #metadata_dump['dig'] = raw.info['dig']
	    #logger.error(metadata_dump['dig'])
	    logger.error('step 1.2.5')
	    metadata_dump['number_of_channels'] = raw.info['nchan']
	    logger.error(raw.info['nchan'])

	    logger.error('step 1.2.6')
	    metadata_dump['number_of_timepoints'] = raw.n_times
	    logger.error(metadata_dump['number_of_timepoints'])	 

	    logger.error('step 1.2.7')
	    metadata_dump['channel_names'] = "".join(raw.ch_names)
	   
            #STI
            numberOfSTI = 0
            for term in raw.ch_names:
                if term.startswith('STI'):
                        numberOfSTI += 1

            metadata_dump['numberOfSTI'] = numberOfSTI
	
	    #EOG
	    numberOfEOG = 0
	    for term2 in raw.ch_names:
		if term2.startswith('EOG'):
			numberOfEOG += 1

	    metadata_dump['numberOfEOG'] = numberOfEOG

	   #EEG
            numberOfEEG = 0
            for term3 in raw.ch_names:
                if term3.startswith('EEG'):
                        numberOfEEG += 1

            metadata_dump['numberOfEEG'] = numberOfEEG

 	    #MEG
	    numberOfMEG = 0
            for term4 in raw.ch_names:
                if term4.startswith('MEG'):
                        numberOfMEG += 1

            metadata_dump['numberOfMEG'] = numberOfMEG

            # get duration
            #metadata_dump['duration'] = raw.duration

            # get sample duration (sampling interval)
            #metadata_dump['sampling_interval'] = raw.info['sampling_interval']

            # get exported raw information
            #metadata_dump['raw_info'] = raw.metadata.keys()

            # get channel names (attribute added during export)
	    #logger.error('step 1.2.10')
            #metadata_dump['channel_names'] = raw.ch_names
            #logger.error(raw.ch_names)
	    #metadata_dump['channel_names'] = raw_ts.ch_names[:3]

            # get The width of the transition band of the highpass filter
            metadata_dump['highpass'] = raw.info['highpass']
	
            # get The width of the transition band of the lowpass filter
            metadata_dump['lowpass'] = raw.info['lowpass']

            logger.error('step 2')
            ###############################################################################

            #Plot graph 
            want_meg = True
            want_eeg = False
            want_stim = False
            include = []
            exclude = raw.info['bads']
            logger.error('step 2.1')

            picks = mne.fiff.pick_types(raw.info, meg=want_meg, eeg=want_eeg,stim=want_stim, include=include, exclude=exclude)
            some_picks = picks[:5]  # take 5 first
            start, stop = raw.time_as_index([0, 15])  # read the first 15s of data
            data, times = raw[some_picks, start:(stop + 1)]
            logger.error('step 2.2')

            import matplotlib.pyplot as pl
            pl.close('all')
            pl.plot(times, data.T)
            pl.xlabel('time (s)')
            pl.ylabel('MEG data (T)')
            logger.error('step 2.3')

            #outputextension = "png"
            #tf = tempfile.TemporaryFile(delete=False)
            #outputfilename = tf.name

            pl.savefig('/opt/mytardis/data/staging/test1.png')
            #tf.close()
            logger.error('step 2.4')

            previewImage64 = self.base64_encode_file('/opt/mytardis/data/staging/test1.png')
            #os.remove(outputfilename)
            logger.error('step 2.5')
            if previewImage64:
                metadata_dump['previewImage'] = previewImage64               
  
            self.saveMetadata(instance, schema, metadata_dump)

        except Exception, e:
            logger.debug(e)
            return None

    def saveMetadata(self, instance, schema, metadata):
        """Save all the metadata to a Dataset_Files parameter set.
        """
	logger.error('MNE-saveMetadata()')
        parameters = self.getParameters(schema, metadata)

        if not parameters:
            return None

        try:
            ps = DatafileParameterSet.objects.get(schema=schema,
                                                  dataset_file=instance)
            return ps  # if already exists then just return it
        except DatafileParameterSet.DoesNotExist:
            ps = DatafileParameterSet(schema=schema,
                                      dataset_file=instance)
            ps.save()

	for p in parameters:
            print p.name
            if p.name in metadata:
                dfp = DatafileParameter(parameterset=ps,
                                        name=p)
                if p.isNumeric():
                    if metadata[p.name] != '':
                        dfp.numerical_value = metadata[p.name]
                        dfp.save()
                else:
                    print p.name
                    if isinstance(metadata[p.name], list):
                        for val in reversed(metadata[p.name]):
                            strip_val = val.strip()
                            if strip_val:
                                if not strip_val in exclude_line:
                                    dfp = DatafileParameter(parameterset=ps,
                                                            name=p)
                                    dfp.string_value = strip_val
                                    dfp.save()
                    else:
                        dfp.string_value = metadata[p.name]
                        dfp.save()

        return ps

    def getParameters(self, schema, metadata):
        """Return a list of the paramaters that will be saved.
        """
        logger.error('MNE-getParameters()')
	param_objects = ParameterName.objects.filter(schema=schema)
        parameters = []
        for p in metadata:

            if self.tagsToFind and not p in self.tagsToFind:
                continue

            if p in self.tagsToExclude:
                continue

            parameter = filter(lambda x: x.name == p, param_objects)

            if parameter:
                parameters.append(parameter[0])
                continue

            # detect type of parameter

 		datatype = ParameterName.STRING

            # Int test
            try:
                int(metadata[p])
            except ValueError:
                pass
            except TypeError:
                pass
            else:
                datatype = ParameterName.NUMERIC

            # Fraction test
            if isinstance(metadata[p], Fraction):
                datatype = ParameterName.NUMERIC

            # Float test
            try:
                float(metadata[p])
            except ValueError:
                pass
            except TypeError:
                pass
            else:
                datatype = ParameterName.NUMERIC

        return parameters

    def getSchema(self):
        """Return the schema object that the paramaterset will use.
        """
	logger.error('MNE-getSchema()')
        try:
            return Schema.objects.get(namespace__exact=self.schema)
        except Schema.DoesNotExist:
            schema = Schema(namespace=self.schema, name=self.name,
                            type=Schema.DATAFILE)
            schema.save()
            return schema

    def base64_encode_file(self, filename):
        """encode file from filename in base64
        """
	logger.error('MNE-base64_encode_file()')
        with open(filename, 'r') as fileobj:
            read = fileobj.read()
            encoded = base64.b64encode(read)

	return encoded

    def exec_command(self, cmd):
        """execute command on shell
        """
	logger.error('MNE-exec_command()')
        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            shell=True)

        p.wait()

        result_str = p.stdout.read()

        return result_str

    def fileoutput(self, cd, execfilename, inputfilename, outputfilename, args=""):
        """execute command on shell with a file output
        """
	logger.error('MNE-fileoutput()')
        cmd = "cd '%s'; ./'%s' '%s' '%s' %s" %\
            (cd, execfilename, inputfilename, outputfilename, args)
        print cmd

        return self.exec_command(cmd)

    def textoutput(self, cd, execfilename, inputfilename, args=""):
        """execute command on shell with a stdout output
        """
	logger.error('MNE-textoutput()')
        cmd = "cd '%s'; ./'%s' '%s' %s" %\
            (cd, execfilename, inputfilename, args)
        print cmd

        return self.exec_command(cmd)

def make_filter(name='', schema='', tagsToFind=[], tagsToExclude=[]):
    logger.error('MNE-make_filter()')
    if not name:
        raise ValueError("MNEImageFilter "
                         "requires a name to be specified")
    if not schema:
        raise ValueError("MNEImageFilter "
                         "requires a schema to be specified")
    return MNEImageFilter(name, schema, tagsToFind, tagsToExclude)
make_filter.__doc__ = MNEImageFilter.__doc__



