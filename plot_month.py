import iris
import iris.plot as iplt
import matplotlib.pyplot as plt
import numpy
import argparse
import iris.coord_categorisation
from provenance import get_history_record

iris.FUTURE.netcdf_promote = True

mask_file = 'sftlf_fx_ACCESS1-3_historical_r0i0p0.nc'
mask_location = data_directory + mask_file

def mask_to_array(input_file,threshold):

    sltlf_cube = iris.load_cube(mask_location, 'land_area_fraction')
    numpy.zeros((sltlf_cube.shape[0],sltlf_cube.shape[1]))
    ocean_mask = numpy.where(sltlf_cube.data<threshold,True,False)
    land_mask = ~ocean_mask
    
    return land_mask,ocean_mask


def plot_month(subset_month,apply_mask,threshold):
    
    #read data
    cube = iris.load_cube(data_location, 'precipitation_flux')
    
    #adjust units
    cube.data = cube.data * 86400
    cube.units = 'mm/day'
    
    #assign mask to variables
    lm, om = mask_to_array(mask_location,threshold)
    
    assert lm.shape == cube.shape, "Mask dimensions for land dont match"
    assert om.shape == cube.shape, "Mask dimensions for ocean dont match"
    
    #apply mask
    if apply_mask == 'Land':
        cube.mask = lm
    if apply_mask == 'Ocean':
        cube.mask = om
    else:
        pass
    
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
    
    mask_file = 'sftlf_fx_ACCESS1-3_historical_r0i0p0.nc'
    mask_location = data_directory + mask_file
    
    data_location = data_directory + file_name
    
    description='Print the input arguments to the screen.'
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument("subset_month", type=str, help="Month to plot")
    
    text_file = open(output_location + "history_log.txt", "w")
    output = get_history_record()
    text_file.write(output

    args = parser.parse_args() 
    
    
    main(args)
    