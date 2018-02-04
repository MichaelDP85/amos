import iris
import iris.plot as iplt
import matplotlib.pyplot as plt
import numpy
import argparse
import iris.coord_categorisation

iris.FUTURE.netcdf_promote = True

def plot_month(subset_month):
    
    #read data
    cube = iris.load_cube(data_location, 'precipitation_flux')
    
    #adjust units
    cube.data = cube.data * 86400
    cube.units = 'mm/day'
    
    #subset month
    iris.coord_categorisation.add_month(cube,'time')
    month_data = cube.extract(iris.Constraint(month=subset_month))
    
    #summarise
    month_mean = month_data.collapsed('time', iris.analysis.MEAN)
    
    #plot
    fig = plt.figure(figsize=[12,5])
    iplt.contourf(month_mean, cmap='viridis_r', levels=numpy.arange(0, 10), extend='max')
    plt.gca().coastlines()
    cbar = plt.colorbar()
    cbar.set_label(str(cube.units))
    plt.title("Mean precipitation climatology - " + subset_month ,fontsize=20)

    plt.savefig(output_location + str(file_name) + "_" + str(subset_month) + ".jpg")

def main(inargs):
    plot_month(inargs)
    
if __name__ == "__main__":
    
    data_directory = '/Users/michael/desktop/data-carpentry/data/'
    file_name = 'pr_Amon_ACCESS1-3_historical_r1i1p1_200101-200512.nc'
    output_location = '/Users/michael/desktop/data-carpentry/output/'
    
    data_location = data_directory + file_name
    
    description='Print the input arguments to the screen.'
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument("subset_month", type=str, help="Month to plot")

    args = parser.parse_args()            
    main(args)
    