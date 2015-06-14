from openmoc import *
import openmoc.log as log
import openmoc.plotter as plotter
import openmoc.materialize as materialize
from openmoc.options import Options


###############################################################################
#######################   Main Simulation Parameters   ########################
###############################################################################

options = Options()

num_threads = options.getNumThreads()
azim_spacing = options.getTrackSpacing()
num_azim = options.getNumAzimAngles()
tolerance = options.getTolerance()
max_iters = options.getMaxIterations()
num_polar = 2
polar_spacing = 2.0
log.set_log_level('NORMAL')
set_line_length(120)

log.py_printf('TITLE', 'Simulating the OECD\'s C5G7 Benchmark Problem...')


###############################################################################
###########################   Creating Materials   ############################
###############################################################################

log.py_printf('NORMAL', 'Importing materials data from HDF5...')

materials = materialize.materialize('../../c5g7-materials.py')


###############################################################################
###########################   Creating Surfaces   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating surfaces...')

xmin = XPlane(x=-32.13, name='xmin')
xmax = XPlane(x= 32.13, name='xmax')
ymin = YPlane(y=-32.13, name='ymin')
ymax = YPlane(y= 32.13, name='ymax')
zmin = ZPlane(z=-32.13, name='zmin')
zmax = ZPlane(z= 32.13, name='zmax')

xmin.setBoundaryType(REFLECTIVE)
xmax.setBoundaryType(VACUUM)
ymin.setBoundaryType(VACUUM)
ymax.setBoundaryType(REFLECTIVE)
zmin.setBoundaryType(REFLECTIVE)
zmax.setBoundaryType(VACUUM)

# Create Circles for the fuel as well as to discretize the moderator into rings
fuel_radius = Circle(x=0.0, y=0.0, radius=0.54)


###############################################################################
######################   Creating Cells and Universes   #######################
###############################################################################

log.py_printf('NORMAL', 'Creating cells...')

# Moderator rings
moderator_ring = Cell()
moderator_ring.setFill(materials['Water'])
moderator_ring.addSurface(+1, fuel_radius)

# UO2 pin cell
uo2_cell = Cell()
uo2_cell.setFill(materials['UO2'])
uo2_cell.addSurface(-1, fuel_radius)

uo2 = Universe(name='UO2')
uo2.addCell(uo2_cell)
uo2.addCell(moderator_ring)

# 4.3% MOX pin cell
mox43_cell = Cell()
mox43_cell.setFill(materials['MOX-4.3%'])
mox43_cell.addSurface(-1, fuel_radius)

mox43 = Universe(name='MOX-4.3%')
mox43.addCell(mox43_cell)
mox43.addCell(moderator_ring)

# 7% MOX pin cell
mox7_cell = Cell()
mox7_cell.setFill(materials['MOX-7%'])
mox7_cell.addSurface(-1, fuel_radius)

mox7 = Universe(name='MOX-7%')
mox7.addCell(mox7_cell)
mox7.addCell(moderator_ring)

# 8.7% MOX pin cell
mox87_cell = Cell()
mox87_cell.setFill(materials['MOX-8.7%'])
mox87_cell.addSurface(-1, fuel_radius)

mox87 = Universe(name='MOX-8.7%')
mox87.addCell(mox87_cell)
mox87.addCell(moderator_ring)

# Fission chamber pin cell
fission_chamber_cell = Cell()
fission_chamber_cell.setFill(materials['Fission Chamber'])
fission_chamber_cell.addSurface(-1, fuel_radius)

fission_chamber = Universe(name='Fission Chamber')
fission_chamber.addCell(fission_chamber_cell)
fission_chamber.addCell(moderator_ring)

# Control rod pin cell
control_rod_cell = Cell()
control_rod_cell.setFill(materials['Control Rod'])
control_rod_cell.addSurface(-1, fuel_radius)

control_rod = Universe(name='Control Rod')
control_rod.addCell(control_rod_cell)
control_rod.addCell(moderator_ring)

# Guide tube pin cell
guide_tube_cell = Cell()
guide_tube_cell.setFill(materials['Guide Tube'])
guide_tube_cell.addSurface(-1, fuel_radius)

guide_tube = Universe(name='Guide Tube')
guide_tube.addCell(guide_tube_cell)
guide_tube.addCell(moderator_ring)

# Reflector
reflector_cell = Cell(name='moderator')
reflector_cell.setFill(materials['Water'])

reflector = Universe(name='Reflector')
reflector.addCell(reflector_cell)

# Cells
assembly_uo2_unrod_cell = Cell(name='UO2 Assembly Unrodded')
assembly_mox_unrod_cell = Cell(name='MOX Assembly Unrodded')
assembly_rfl_unrod_cell = Cell(name='Reflector Unrodded')
assembly_rfl_rod_cell = Cell(name='Reflector Rodded')

assembly_uo2_unrod = Universe(name='UO2 Assembly Unrodded')
assembly_mox_unrod = Universe(name='MOX Assembly Unrodded')
assembly_rfl_unrod = Universe(name='Rfl Assembly Unrodded')
assembly_rfl_rod = Universe(name='Rfl Assembly Rodded')

assembly_uo2_unrod.addCell(assembly_uo2_unrod_cell)
assembly_mox_unrod.addCell(assembly_mox_unrod_cell)
assembly_rfl_unrod.addCell(assembly_rfl_unrod_cell)
assembly_rfl_rod.addCell(assembly_rfl_rod_cell)

# Root Cell/Universe
root_cell = Cell(name='Full Geometry')
root_cell.addSurface(halfspace=+1, surface=xmin)
root_cell.addSurface(halfspace=-1, surface=xmax)
root_cell.addSurface(halfspace=+1, surface=ymin)
root_cell.addSurface(halfspace=-1, surface=ymax)
root_cell.addSurface(halfspace=+1, surface=zmin)
root_cell.addSurface(halfspace=-1, surface=zmax)

root_universe = Universe(name='Root Universe')
root_universe.addCell(root_cell)


###############################################################################
###########################   Creating Lattices   #############################
###############################################################################

log.py_printf('NORMAL', 'Creating lattices...')

lattices = list()

# UO2 unrodded 17 x 17 assemblies
lattices.append(Lattice(name='Assembly UO2 Unrodded'))
lattices[-1].setWidth(width_x=1.26, width_y=1.26, width_z=7.14)
template = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1],
            [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 2, 1, 1, 2, 1, 1, 3, 1, 1, 2, 1, 1, 2, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
            [1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

universes = {1 : uo2, 2 : guide_tube, 3 : fission_chamber}
for i in range(17):
  for j in range(17):
    template[i][j] = universes[template[i][j]]
lattices[-1].setUniverses(template)
assembly_uo2_unrod_cell.setFill(lattices[-1])

# MOX unrodded 17 x 17 assemblies
lattices.append(Lattice(name='Assembly MOX Unrodded'))
lattices[-1].setWidth(width_x=1.26, width_y=1.26, width_z=7.14)
template = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 4, 2, 2, 4, 2, 2, 4, 2, 2, 2, 2, 1],
            [1, 2, 2, 4, 2, 3, 3, 3, 3, 3, 3, 3, 2, 4, 2, 2, 1],
            [1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 1],
            [1, 2, 4, 3, 3, 4, 3, 3, 4, 3, 3, 4, 3, 3, 4, 2, 1],
            [1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 1],
            [1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 1],
            [1, 2, 4, 3, 3, 4, 3, 3, 5, 3, 3, 4, 3, 3, 4, 2, 1],
            [1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 1],
            [1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 1],
            [1, 2, 4, 3, 3, 4, 3, 3, 4, 3, 3, 4, 3, 3, 4, 2, 1],
            [1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 1],
            [1, 2, 2, 4, 2, 3, 3, 3, 3, 3, 3, 3, 2, 4, 2, 2, 1],
            [1, 2, 2, 2, 2, 4, 2, 2, 4, 2, 2, 4, 2, 2, 2, 2, 1],
            [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

universes = {1 : mox43, 2 : mox7, 3 : mox87,
             4 : guide_tube, 5 : fission_chamber}
for i in range(17):
  for j in range(17):
    template[i][j] = universes[template[i][j]]
lattices[-1].setUniverses(template)
assembly_mox_unrod_cell.setFill(lattices[-1])

# Reflector rodded 17 x 17 assemblies
lattices.append(Lattice(name='Assembly Reflector Rodded'))
lattices[-1].setWidth(width_x=1.26, width_y=1.26, width_z=7.14)
template = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1],
            [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 2, 1, 1, 2, 1, 1, 3, 1, 1, 2, 1, 1, 2, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
            [1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

universes = {1 : reflector, 2 : control_rod, 3 : fission_chamber}
for i in range(17):
  for j in range(17):
    template[i][j] = universes[template[i][j]]
lattices[-1].setUniverses(template)
assembly_rfl_rod_cell.setFill(lattices[-1])

# Reflector unrodded assembly
lattices.append(Lattice(name='Assembly Reflector Unrodded'))
lattices[-1].setWidth(width_x=1.26, width_y=1.26, width_z=7.14)
template = [[reflector] * 17] * 17
lattices[-1].setUniverses(template)
assembly_rfl_unrod_cell.setFill(lattices[-1])

# 3 x 3 x 9 core to represent 3D core
lattices.append(Lattice(name='Full Geometry'))
lattices[-1].setWidth(width_x=21.42, width_y=21.42, width_z=7.14)
lattices[-1].setUniverses3D([[[assembly_rfl_rod  , assembly_rfl_rod  , assembly_rfl_unrod],
                              [assembly_rfl_rod  , assembly_rfl_rod  , assembly_rfl_unrod],
                              [assembly_rfl_unrod, assembly_rfl_unrod, assembly_rfl_unrod]],
                             [[assembly_rfl_rod  , assembly_rfl_rod  , assembly_rfl_unrod],
                              [assembly_rfl_rod  , assembly_rfl_rod  , assembly_rfl_unrod],
                              [assembly_rfl_unrod, assembly_rfl_unrod, assembly_rfl_unrod]],
                             [[assembly_rfl_rod  , assembly_rfl_rod  , assembly_rfl_unrod],
                              [assembly_rfl_rod  , assembly_rfl_rod  , assembly_rfl_unrod],
                              [assembly_rfl_unrod, assembly_rfl_unrod, assembly_rfl_unrod]],
                             [[assembly_uo2_unrod, assembly_mox_unrod, assembly_rfl_unrod],
                              [assembly_mox_unrod, assembly_uo2_unrod, assembly_rfl_unrod],
                              [assembly_rfl_unrod, assembly_rfl_unrod, assembly_rfl_unrod]],
                             [[assembly_uo2_unrod, assembly_mox_unrod, assembly_rfl_unrod],
                              [assembly_mox_unrod, assembly_uo2_unrod, assembly_rfl_unrod],
                              [assembly_rfl_unrod, assembly_rfl_unrod, assembly_rfl_unrod]],
                             [[assembly_uo2_unrod, assembly_mox_unrod, assembly_rfl_unrod],
                              [assembly_mox_unrod, assembly_uo2_unrod, assembly_rfl_unrod],
                              [assembly_rfl_unrod, assembly_rfl_unrod, assembly_rfl_unrod]],
                             [[assembly_uo2_unrod, assembly_mox_unrod, assembly_rfl_unrod],
                              [assembly_mox_unrod, assembly_uo2_unrod, assembly_rfl_unrod],
                              [assembly_rfl_unrod, assembly_rfl_unrod, assembly_rfl_unrod]],
                             [[assembly_uo2_unrod, assembly_mox_unrod, assembly_rfl_unrod],
                              [assembly_mox_unrod, assembly_uo2_unrod, assembly_rfl_unrod],
                              [assembly_rfl_unrod, assembly_rfl_unrod, assembly_rfl_unrod]],
                             [[assembly_uo2_unrod, assembly_mox_unrod, assembly_rfl_unrod],
                              [assembly_mox_unrod, assembly_uo2_unrod, assembly_rfl_unrod],
                              [assembly_rfl_unrod, assembly_rfl_unrod, assembly_rfl_unrod]]])


root_cell.setFill(lattices[-1])


###############################################################################
##########################     Creating Cmfd mesh    ##########################
###############################################################################

log.py_printf('NORMAL', 'Creating Cmfd mesh...')

cmfd = Cmfd()
cmfd.setMOCRelaxationFactor(1.0)
cmfd.setSORRelaxationFactor(1.5)
cmfd.setLatticeStructure(51,51,1)
cmfd.setGroupStructure([1,4,8])
cmfd.setKNearest(4)


###############################################################################
##########################   Creating the Geometry   ##########################
###############################################################################

log.py_printf('NORMAL', 'Creating geometry...')

geometry = Geometry()
geometry.setRootUniverse(root_universe)
geometry.setCmfd(cmfd)
geometry.initializeFlatSourceRegions()

###############################################################################
########################   Creating the TrackGenerator   ######################
###############################################################################

log.py_printf('NORMAL', 'Initializing the track generator...')

quad = EqualAnglePolarQuad()
quad.setNumPolarAngles(num_polar)

track_generator = TrackGenerator(geometry, num_azim, num_polar, azim_spacing, polar_spacing)
track_generator.setQuadrature(quad)
track_generator.setNumThreads(num_threads)
#track_generator.setSolve2D()
track_generator.setZLevel(0.1)
track_generator.generateTracks()

#plotter.plot_materials(geometry, gridsize=500, plane='xy', offset=0.)
#plotter.plot_cells(geometry, gridsize=500, plane='xy', offset=0.)
#plotter.plot_flat_source_regions(geometry, gridsize=500, plane='xy', offset=0.)
#plotter.plot_cmfd_cells(geometry, cmfd, gridsize=500, plane='xy', offset=0.)


###############################################################################
###########################   Running a Simulation   ##########################
###############################################################################

solver = CPUSolver(track_generator)
solver.setConvergenceThreshold(tolerance)
solver.setNumThreads(num_threads)
solver.computeEigenvalue(max_iters)
solver.printTimerReport()


###############################################################################
############################   Generating Plots   #############################
###############################################################################

log.py_printf('NORMAL', 'Plotting data...')

#plotter.plot_spatial_fluxes(solver, energy_groups=[1,2,3,4,5,6,7],
#                            gridsize=500, plane='xy', offset=0.)
#plotter.plot_spatial_fluxes(solver, energy_groups=[1,2,3,4,5,6,7],
#                            gridsize=500, plane='xz', offset=0.)
#plotter.plot_spatial_fluxes(solver, energy_groups=[1,2,3,4,5,6,7],
#                            gridsize=500, plane='yz', offset=0.)

#plotter.plot_materials(geometry, gridsize=500)
#plotter.plot_cells(geometry, gridsize=500)
#plotter.plot_flat_source_regions(geometry, gridsize=500)
#plotter.plot_spatial_fluxes(solver, energy_groups=[1,2,3,4,5,6,7])
#plotter.plot_segments_3d(track_generator)

log.py_printf('TITLE', 'Finished')
