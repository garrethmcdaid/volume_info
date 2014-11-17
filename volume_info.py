import sys
import boto.ec2

#GET COMMAND LINE ARGUMENTS
a = sys.argv

#CONNECTION
ec2 = boto.ec2.connect_to_region(a[1])

#ARRAY OF VOLUMES
vol = ec2.get_all_volumes()

#TOTAL HOLDERS
total = 0
total_attached = 0
total_available = 0
total_no_attached = 0
total_no_available = 0
total_iops = 0
total_no_iops = 0
total_no_non_iops = 0


#ARRAYS
zone = {}

for v in vol:
    total += v.size
    
    try:
        v.iops += 1
        total_iops += v.iops
        total_no_iops += 1
    except TypeError:
        total_no_non_iops += 1

    if v.zone not in zone:
        zone[v.zone] = {}
            
    if "attached" not in zone[v.zone]:
    	zone[v.zone]["attached"] = 0

    if "available" not in zone[v.zone]:
    	zone[v.zone]["available"] = 0

    if "total" not in zone[v.zone]:
    	zone[v.zone]["total"] = 0

    zone[v.zone]["total"] += v.size
    
    if v.attachment_state() == "attached":
        total_attached += v.size
        total_no_attached += 1
        zone[v.zone]["attached"] += v.size
    else:
    	total_available += v.size
    	total_no_available += 1
    	zone[v.zone]["available"] += v.size
    	
print "Region: %s" % (a[1])    	
    	
print "Total Volumes: " + "{0:,}".format(len(vol))
print "Total Volume Size in GB: " + "{0:,}".format(total) + " (" + "{0:,}".format(len(vol)) + " Volumes)"
print "Total Attached Volume Size in GB: " + "{0:,}".format(total_attached) + " (" + "{0:,}".format(total_no_attached) + " Volumes)"
print "Total Available Volume Size in GB: " + "{0:,}".format(total_available) + " (" + "{0:,}".format(total_no_available) + " Volumes)"
print "Total Provisioned IOPS: " + "{0:,}".format(total_iops) + " (" + "{0:,}".format(total_no_iops) + " Volumes)"

for z in zone:
	print z + ": Attached = " + str(zone[z]["attached"]) + ": Available = " + str(zone[z]["available"]) + ": Total = " + str(zone[z]["total"])

