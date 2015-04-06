import re
import pg

try:
  conn = pg.connect(host="192.168.100.200", dbname="ytwen", user="ytwen", passwd="woodcar")
except:
  print "I am unable to connect to the database"

spatialAnomaly = 0
sequentialAnomaly = 0
behavioralAnomaly = 0
minTs = 10
minSus = 0.01
# Anomany search
# file_r = open('evaluation_sequence','r')
# for line in file_r.readlines():
#   pattern = re.findall('([0-9 ]+)',line)
#   grids = pattern[1].split(' ')

#   # 1.spatial
#   gridSize = len(grids);
#   #sql_grids = ''
#   for grid in grids:
#     sqlResult = conn.query( "select counter from mtas.pst_exp where pattern like '%s '" % (grid) ).getresult()
#   #  sql_grids += "'"+str(grid) + " ',"
#   #sql_grids += "''"
#   #frequent = conn.query( "select count(*) from mtas.pst_exp where pattern in (%s) and counter >= %d" % (sql_grids,minTs) ).getresult()[0][0]
#   # anomaly
#   #if gridSize !=  frequent:
#     # no pst record: prob = 0
#     if sqlResult == []:
#       gridProb = 0
#     else:
#       gridProb = sqlResult[0][0]
#     if gridProb < minTs:
#       print "spatial %s select counter from mtas.pst_exp where pattern like '%s '" % (line,grid)
#       spatialAnomaly += 1
#       break
#   #else:
#     #print(line+str(frequent))
#   # 2. sequential
#   for i in range(1,len(grids)):
#     seqNode = str(grids[i-1])+' '+str(grids[i])+' '
#     sqlResult = conn.query("select prob from mtas.pst_exp where pattern like ('%s')" % seqNode).getresult()
#     # no pst record: prob = 0
#     if sqlResult == []:
#       seqProb = 0
#     else:
#       seqProb = sqlResult[0][0]
#     # anomaly
#     if seqProb < minSus:
#       print pattern[0]+':'+seqNode+"anomaly "+str(seqProb)
#       print "select prob from mtas.pst_exp where pattern like ('%s')" % seqNode
#       sequentialAnomaly += 1
#       break
  #break
# 3. behavioral 
file_r = open('evaluation_behavior_pre.csv','r')
tidIsAnomaly = False
for line in file_r.readlines():
  # list comprehension
  # 0:tid,1: pattern, 2:next, 3:cog, 4:sog
  record = [x.strip() for x in line.split(',')]
  # preliminary sql
  # insert into mtas.pst_table_exp 
  #   (select pattern,next,array[avg(cog),avg(sog)] as bc_mean,array[stddev_pop(cog),stddev_pop(sog)] as bc_stddev 
  #      from mtas.pst_table_pre_exp group by pattern,next)
  # this tid is checked anomaly
  if tidIsAnomaly and record[0]==tid:
    continue
  else:
    tidIsAnomaly = False
  tid = record[0]
  # cog_mean, sog_mean, cog_stddev, sog_stddev
  sqlResult = conn.query("SELECT bc_mean[1],bc_mean[2],bc_stddev[1],bc_stddev[2], cog_mean FROM mtas.pst_table_exp WHERE pattern = '%s' AND next = %s" % (record[1],record[2]) ).getresult()
  
  # first occur: no bc check
  if sqlResult == []:
    #behavioralAnomaly += 1
    continue
  else:
    bc = sqlResult[0]
  # check cog
  # cog = float(record[3])
  # if cog < 0:
  #   cog += 360
  if bc[4] - 2*bc[2] <= float(record[3]) <= bc[4] + 2*bc[2] or bc[4] - 2*bc[2] <= float(record[3])+360 <= bc[4] + 2*bc[2]: #if bc[0] - 2*bc[2] <= float(cog) <= bc[0] + 2*bc[2]:#
  # check sog
    if bc[1] - 2*bc[3] <= float(record[4]) <= bc[1] + 2*bc[3]:
      continue
  tidIsAnomaly = True
  print "%s anomaly grid = %s %s" % (tid,record[1],record[2])
  print "cog = %s sog = %s mean = %s(%s),%s stddev = %s,%s" % (record[3],record[4],bc[0],bc[4],bc[1],bc[2],bc[3])
  behavioralAnomaly += 1
  # break

print spatialAnomaly
print sequentialAnomaly
print behavioralAnomaly

