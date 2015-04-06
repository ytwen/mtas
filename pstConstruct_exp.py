import re
# given ship_sequence, construct PST
# 1. run web (frequent_sequence.php) to consturct input files
# 2. run this, output pst (& bc_pre csv)
# 3. import pst
#    \copy mtas.pst_exp from '/home/ytwen/MTAS/pst_exp.csv' with delimiter ','
#    \copy mtas.pst_table_pre_exp from '/home/ytwen/MTAS/pst_table_pre_exp.csv' with delimiter ','
# 4. run sql: insert into mtas.pst_table_exp (
#      select pattern,next,array[avg(cog),avg(sog)] as bc_mean,array[stddev_pop(cog),stddev_pop(sog)] as bc_stddev 
#        from mtas.pst_table_pre_exp group by pattern,next having count(*) > 1);

file_r = open('ship_sequence_input','r')
lineCount = sum(1 for line in open('ship_sequence_input','r'))
file_w = open('pst_exp.csv','w')
pst = dict()
# file.wirte(line);
for line in file_r.readlines():
  pattern = re.findall('([0-9 ]+)',line)
  grids = pattern[1].split(' ')
  # build node pattern
  for i in range(0,len(grids)):
    for j in range(i,-1,-1):
      node = ''
      for k in range (j,i+1):
        node += str(grids[k])+' '
      #print(node)
      if node in pst:
      	pst[node]+=1
      else:
      	pst[node]=1
    #node = str(grids[i])+' '
  #print(pst)
  #break

file_r.close()

for nodePattern,count in pst.iteritems():
  # prob computation
  parrentIndex = nodePattern.rfind(" ",0,len(nodePattern)-1)
  # multi grid
  if parrentIndex != -1:
    parrent = nodePattern[ :parrentIndex]
    parrentCount = pst[parrent+' ']
    #print(nodePattern+','+str(count)+' parrent='+parrent+str()+'\n')
  # 1grid
  else:
    #print(nodePattern+','+str(count)+'\n')
    parrentCount = lineCount
  prob = count / float(parrentCount)
  line = "%s,%d,%f\n" % (nodePattern,count,prob)
  file_w.write(line)

file_w.close()