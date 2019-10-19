from opentrons import instruments, containers, robot
from opentrons.util import environment
from opentrons.util.vector import Vector
from math import *

#INIT THE MACHINE(connection + port)
def initall():
	robot.connect(robot.get_serial_ports_list()[0])
	robot.is_connected()
	robot.home()

#####################################################################################

#Inital all variables
trash = containers.load('point', 'A1')
tiprack = containers.load('tiprack-200ul', 'A3')

water_1 = containers.load('point', 'B3')
water_2 = containers.load('point', 'C3')
water_3 = containers.load('point', 'D3')

pcr96_1 = containers.load('96-PCR-flat', 'B1')
pcr96_2 = containers.load('96-PCR-flat', 'C1')
pcr96_3 = containers.load('96-PCR-flat', 'D1')

petri_1 = containers.load('point', 'B2')
petri_2 = containers.load('point', 'C2')
petri_3 = containers.load('point', 'D2')

pipette = instruments.Pipette(
	axis='b',
	min_volume=20,
	max_volume=200,
	tip_racks=[tiprack],
	trash_container=trash,
	)

#load variables into array
pcr = [pcr96_1, pcr96_2, pcr96_3]
water = [water_1, water_2, water_3]
petri = [petri_1, petri_2, petri_3]
#####################################################################################

#THE MAIN PROGRAM STARTS HERE

def mainprogram(timez):
	pipette.drop_tip(trash)
	for each in range(timez):
		a, b = 5, 1
		petri_diameter = 85
		theta = 1
		deltaincrease = (petri_diameter / 2 - 2 - a) / b / len(pcr96_1.wells())

		#pick up the tip from the tiprack, the variable each will do the next one
		pipette.pick_up_tip(tiprack.wells(each))

		#loop through each well
		for well in range(96):

			#get water from the water trough
			pipette.aspirate(100, water[each])

            #this portion is to calculate xy coordinates from polar coordinates to find circle
			#a turns the spiral, while b controls the distance between successive turnings
			r = a + b * theta
			x = r * cos(theta)
			y = r * sin(theta)
			theta += deltaincrease


        #these steps are to pick up yeast samples and put them in a sample tray
########################################################################################
			pipette.move_to(( petri[each], Vector(
				petri[each]._coordinates.coordinates.x + x,
				petri[each]._coordinates.coordinates.y + y,
				petri[each]._coordinates.coordinates.z
			)), 'arc' )

			pipette.aspirate(100)

			pipette.move_to(( petri[each], Vector(
				petri[each]._coordinates.coordinates.x + x - 1,
				petri[each]._coordinates.coordinates.y + y - 1,
				petri[each]._coordinates.coordinates.z
			)), 'direct' )

			pipette.move_to(( petri[each], Vector(
				petri[each]._coordinates.coordinates.x + x + 2,
				petri[each]._coordinates.coordinates.y + y + 2,
				petri[each]._coordinates.coordinates.z
			)), 'direct' )

			pipette.dispense(200, pcr[each].wells(well).bottom())
#######################################################################################

		#drop pippete into trash 
		pipette.drop_tip(trash)

initall()
mainprogram(3)


