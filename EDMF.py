"""EDMF class.
An implementation of the main functions of EDMF



Author: Alberto Costa
Institution: Future Cities Laboratory, Singapore
Version: 0.1
Last modify: 06/03/18
"""

import numpy as np
import pandas as pd
import os.path


class EDMF:

    """
    Class with all the functions to read data and implement the EDMF procedure

    """


    def __init__(self, xlsx_filename, n_param):


        # check if file exists
        assert (os.path.isfile(xlsx_filename) == True)

        #filename
        self.xlsx_filename = xlsx_filename

        # array of measurements (num_sensors x 1)
        self.measurements = np.array([])

        # matrix of predictions (size_IMS x num_sensors)
        self.predictions = np.array([])

        # matrix of parameters (size_IMS x num_parameters)
        self.parameters = np.array([])

        # indices of models (from 1 to size_IMS) in the CMS
        self.CMS = list()

        # number of parameters
        self.num_parameters = n_param

        # number of sensors
        self.num_sensors = 0

        # number of simulations
        self.size_IMS = 0

        # list of names of parameters
        self.name_parameters = list()

        # list of names of sensors
        self.name_sensors = list()

        # list of distributions, one for each sensor, for prediction errors
        self.distributions_pred = np.array([])

        # list of distributions, one for each sensor, for measurement errors
        self.distributions_meas = np.array([])

        # T low, T high values
        self.T = np.array([])


        # number of samples for the Monte Carlo simulation
        #self.Monte_Carlo_samples = settings.Monte_Carlo_samples

        # cutoff values for computing the values of T_low and T_high (e.g., for 95%  use 95)
        #self.cutoff_T = settings.cutoff_T



        # initialize the measurements
        self.read_meas()

        # initialize the predictions and parameters
        self.read_pred()

        # assign the dimensions (num_sensors, size_IMS) from data read
        self.num_sensors = len(self.name_sensors)
        self.size_IMS = self.predictions.shape[0]

        assert(self.predictions.shape[1]==self.num_sensors)
        assert(self.parameters.shape[0]==self.size_IMS)


        self.print_statistisc()


        # -- end function






    def read_meas(self):

        """
        Function that reads the Excel file containing the measurements
        :param xlsx_filename: file name (with path). Must have sheets "Pred", "Meas", Pred_Err", and "Meas_Err"
        :return: vector of measurements
        """

        # check if file exists
        #assert (os.path.isfile(self.xlsx_filename) == True)

        xl = pd.ExcelFile(self.xlsx_filename)
        df = xl.parse("Meas")
        self.measurements = df.values

        # -- end functions





    def read_pred(self):

        """
        Function that reads the Excel file containing the predictions
        :param xlsx_filename: file name (with path). Must have sheets "Pred", "Meas", Pred_Err", and "Meas_Err"
        :param n_param: number of parameters of the model. The first n_param columns are parameters, the rest are the corresponding predictions
        :return: matrix of samples (1 row for each sample, 1 col for each param) and matrix of corresponding predictions
        """

        # check if file exists
        #assert (os.path.isfile(self.xlsx_filename) == True)

        xl = pd.ExcelFile(self.xlsx_filename)
        df = xl.parse("Pred")

        #parameters info
        par = df.iloc[:, range(0, self.num_parameters)]
        self.parameters = par.values
        self.name_parameters = list(par)

        #predictions info
        pre = df.iloc[:, self.num_parameters:]
        self.predictions = pre.values
        self.name_sensors = list(pre)



        # -- end function



    def Monte_Carlo_sampling(self, type, xlsx_filename=None, n_samples=1000000):
        """
        For measurements or predictions compute the combined distribution for each sensor, by summing the monte carlo sampling
        results obtained with all the errors specified in the file

        Compute T_low and T_high for falsification. Pred + U_pred = Meas + U_meas. P-M = U_meas - U_pred. With Monte Carlo
        draw 1 random sample from U_meas (unif. distr. within bounds) and 1 from U_pred. Subtract second one from first one. Repeat
        n_samples times. Take the lower and upper bounds of the obtained distribution that keep inside 95% of the values.
        :param type: m for measurements, p for predictions
        :param xlsx_filename: filename with error specification
        :param n_samples: number of samples of Monte Carlo Sampling
        """
        # check if data is correct, if not throw error
        assert(type == 'm' or type =='p')

        #if no input file provided, use that of the class
        if xlsx_filename == None:
            xlsx_filename = self.xlsx_filename
        else:
            assert (os.path.isfile(self.xlsx_filename) == True)

        xl = pd.ExcelFile(self.xlsx_filename)

        # measurement case
        if type == 'm':
            df = xl.parse("Meas_Err")
            # mean for relative uniform case
            mean = self.measurements
            self.distributions_meas = np.zeros([self.num_sensors,n_samples])

        else: #prediction case
            df = xl.parse("Pred_Err")
            mean = self.predictions.mean(axis=0)
            self.distributions_pred = np.zeros([self.num_sensors, n_samples])


        # check if nr columns is correct
        assert len(df.columns)-3 == self.num_sensors



        error_data = df.values


        # compute combine distributions (using different errors) for each sensor
        for j in range(3,self.num_sensors+3): #scan sensors
            tmp_distr = np.zeros(n_samples)
            for i in range (0,df.shape[0]): #scan errors
                # 0/1 values for use/not use sensors
                if error_data[i,j] == 1:
                    if error_data[i,2] == 'r':
                        #relative case
                        tmp_distr = tmp_distr + np.random.uniform(error_data[i,0]*mean[j-3], error_data[i,1]*mean[j-3], n_samples)
                    elif error_data[i,2] =='a':
                        #absolute case
                        tmp_distr = tmp_distr + np.random.uniform(error_data[i, 0], error_data[i, 1], n_samples)
                    else:
                        #gaussian case
                        tmp_distr = tmp_distr + np.random.normal(error_data[i, 0], error_data[i, 1], n_samples)
            if type == 'm':
                self.distributions_meas[j-3] = tmp_distr
            else:
                self.distributions_pred[j-3] = tmp_distr



    def T_bounds(self, Sidak=True, cutoff = 95):

        """
        Compute T_low, T_high for each sensor

        :param sidak: If True use Sidak correction, if False no
        :param cutoff: value for cutoff for computing T_low, T_high
        :return: NULL
        """

        assert(Sidak==True or Sidak==False)
        assert(cutoff>0 and cutoff<100)

        if Sidak==True:
            cutoff = 100.0 * (cutoff/100.0) ** (1.0/self.num_sensors)

            #TO CHECK SIDAK


        self.T = np.zeros([self.num_sensors, 2])
        for s in range(self.num_sensors):

            distribution = self.distributions_meas[s] - self.distributions_pred[s]
            self.T[s, 0] = np.percentile(distribution, (100.0 - 1.0 * cutoff) / 2.0)  # T_low
            self.T[s, 1] = np.percentile(distribution, (100.0 + 1.0 * cutoff) / 2.0)  # T_high




    def falsification(self):
        """
        Perform the falsification

        :return: NULL
        """

        pm = self.predictions - self.measurements.T

        for s in range(self.size_IMS):
            if np.all(pm[s, :] - self.T[:, 1] <= 0) and np.all(pm[s, :] - self.T[:, 0] >= 0):
                self.CMS.append(s)


    def save_CMS(self, xlsx_output):
        """

        Save the IDs, parameters, and predictions of the candidate models in the xlsx_output file
        :param xlsx_output: xlsx output file where the CMS will be saved. NB index ID is 0 to end-1
        :return: NULL
        """

        col = ["ID"]
        for i in range(0, self.num_parameters):
            col.append(self.name_parameters[i])
        for i in range(0, self.num_sensors):
            col.append(self.name_sensors[i])

        result = pd.DataFrame(columns=col)

        result['ID'] = self.CMS

        #result.insert[range(self.num_parameters)] = \
        #print self.parameters[self.CMS]

        result.loc[:,self.name_parameters] = self.parameters[self.CMS]
        result.loc[:, self.name_sensors] = self.predictions[self.CMS]

        writer = pd.ExcelWriter(xlsx_output, engine='xlsxwriter')
        result.to_excel(writer, sheet_name="CMS", index=False)
        writer.save()





















        #
        # assert (isinstance(U_pred, np.ndarray))  # use this, not np.array
        # assert (isinstance(U_meas, np.ndarray))
        # assert (U_pred.shape[1] == 2)  # 2 columns
        # assert (U_meas.shape[1] == 2)  # 2 columns
        # assert (U_meas.shape[0] == U_pred.shape[0])  # same nr of rows (nr sensors tested)
        #
        # n_sensors = U_meas.shape[0]
        # T = np.zeros([n_sensors, 2])  # matrix with results
        #
        # for s in range(n_sensors):
        #     sample_pred = np.random.uniform(U_pred[s, 0], U_pred[s, 1], n_samples)
        #     sample_meas = np.random.uniform(U_meas[s, 0], U_meas[s, 1], n_samples)
        #     distribution = sample_meas - sample_pred
        #     T[s, 0] = np.percentile(distribution, (100.0 - 1.0 * cutoff) / 2.0)  # T_low
        #     T[s, 1] = np.percentile(distribution, (100.0 + 1.0 * cutoff) / 2.0)  # T_high
        #
        # return T






    #def read_error_meas(self):








    def print_statistisc(self):

        """
        Function that prints statistics about the object created

        :return: NULL
        """

        print "\n-----"
        print "Object succesfully created. Report:\n"

        print "Filename: " + self.xlsx_filename + "\n"
        print "Number of sensors: " + str(self.num_sensors) + "\n"
        print "Sensors IDs: " + str(self.name_sensors) + "\n"
        print "Number of parameters: " + str(self.num_parameters) + "\n"
        print "Parameters IDs: " + str(self.name_parameters) + "\n"
        print "Number of simulations (IMS size): " + str(self.size_IMS)
        print "-----\n"


        # -- end function







