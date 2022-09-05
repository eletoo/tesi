# I used the Fitter library which uses SciPy library for distribution fitting and supports 80 distributions
import os

from fitter import Fitter, get_common_distributions, get_distributions


def fit_data_by_sc(df, distributions):
    if not os.path.exists("fit_by_sc_2"):
        os.mkdir("fit_by_sc_2")

    if not os.path.exists("fit_by_sc"):
        os.mkdir("fit_by_sc")

    if not os.path.exists(os.path.join(os.getcwd(), "fit_increments", "Values")):
        os.mkdir(os.path.join(os.getcwd(), "fit_increments", "Values"))

    # fit(df, fitter.get_common_distributions(), 'fit_by_sc')
    # fit(df, distributions, 'fit_by_sc_2')
    fit_increments(df.diff().drop(labels=0, axis=0), distributions, 'fit_increments')


def fit(df, distributions, path):
    for title in df:
        f = Fitter(df[title] - df[title].mean(), xmin=-150, xmax=150, bins=100,
                   distributions=distributions.keys(),
                   timeout=30, density=True)
        f.fit()
        print("fitting " + title)
        f.summary().to_csv(os.path.join(path, 'Fitting' + title + '.csv'), sep='\t', index=True)


def fit_increments(df, distributions, path):
    for title in df:
        print("fitting increments " + title)
        f = Fitter(df[title] - df[title].mean(), xmin=-150, xmax=150, bins=100,
                   distributions=distributions.keys(),
                   timeout=30, density=True)

        file = open(
            os.path.join(path, 'Values', 'Parameters of distributions after fitting ' + title + 'Increments.txt'), "w")
        fit_distributions_and_save_params(distributions, f, file)
        f.summary().to_csv(os.path.join(path, 'Best five distributions fitting' + title + 'Increments.csv'), sep='\t',
                           index=True)


def fit_distributions_and_save_params(distributions, f, file):
    f.fit()
    for dist, values in f.fitted_param.items():
        file.write(f"{dist} - (")
        params = [x.name for x in distributions.get(dist)._shape_info()] + ["location", "scale"]
        for pname, pval in zip(params, values):
            file.write("{}:\t{:.8f}\t".format(pname, pval))
        file.write(")\n")
    file.close()


def find_best_dist(df, distributions, path):
    file = open(
        os.path.join(path, 'Best-fitting_distributions'), "w")
    for title in df:
        print("fitting increments " + title)
        f = Fitter(df[title] - df[title].mean(), xmin=-150, xmax=150, bins=100,
                   distributions=distributions.keys(),
                   timeout=30, density=True)
        f.fit()
        file.write("{}:\t{}\n".format(title, f.get_best("sumsquare_error")))
