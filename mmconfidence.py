import numpy as np

def get_confidence_level():

    Z = 1.645
    # Need to run the other 2 tonight, then put them in this list
    prefix_list = ["Lmda2Init7", "Lmda2Init0", "Lmda10Init4", "Lmda10Init0"]
    file_name = 'confidence_level.txt'
    output = open(file_name, 'a')

    for prefix in prefix_list:
        file_blocking = prefix + "_blocking.txt"
        file_spending = prefix + "_spending.txt"
        file_num_customers = prefix + "_num_customers.txt"

        output.write('#####################################################\n')
        output.write('######### System configuration %s #########\n' % prefix)
        output.write('#####################################################\n')

        #Blocking Probability
        blocking = np.loadtxt(open(file_blocking, 'rb'))
        length_blocking = len(blocking)
        mean_blocking = np.mean(blocking)
        # This is sample variance for estimator
        var_blocking = np.var(blocking) * length_blocking / (length_blocking-1)
        error_blocking = Z * np.sqrt(var_blocking/len(blocking))
        output.write('Mean blocking probability:    %.6f +- %.6f\n' \
                     % (mean_blocking, error_blocking))

        #Mean Spending time
        spending = np.loadtxt(open(file_spending, 'rb'))
        length_spending = len(spending)
        mean_spending = np.mean(spending)
        # This is sample variance for estimator
        var_spending = np.var(spending) * length_spending / (length_spending-1)
        error_spending = Z * np.sqrt(var_spending/len(spending))
        output.write('Mean spending time in system: %.6f +- %.6f\n' \
                     % (mean_spending, error_spending))

        #mean number of customers
        num_customers = np.loadtxt(open(file_num_customers, 'rb'))
        length_num_customers = len(num_customers)
        mean_num_customers = np.mean(num_customers)
        # This is sample variance for estimator
        var_num_customers = np.var(num_customers) * length_num_customers \
            / (length_num_customers-1)
        error_num_customers = Z * np.sqrt(var_num_customers/len(num_customers))
        output.write('Mean # of packets in system:  %.6f +- %.6f\n' \
                     % (mean_num_customers, error_num_customers))
        output.write('#####################################################\n')
        output.write('\n')

