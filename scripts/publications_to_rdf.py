import csv
import itertools
f1 = open('papers_1_pub_new.csv', 'r')
f2 = open('papers_1.csv', 'r')
f3=open('papers_1.csv', 'r')
c1 = csv.reader(f1)
c2 = csv.reader(f2)
c3=csv.reader(f3)
count=0
for row1, row2 in zip(c1,c2):
	   
	   if count !=0:
	   	ref_id=row1[0]
	   	paper_name=row1[1]
	   	year=row1[2]
	   	authors_id=row1[-1]
	   	#print(authors_id)
	   	split_author_id=authors_id.split(',')
	   	full_authors=''
	   	for e in split_author_id:
	   		full_authors+='adage:'+e+','
	   	full_authors=full_authors[:-1]
	   	f=open("new.ttl", "a+")
	   	f.write("adage:"+ref_id+" a fabio:ResearchPaper;\n")
	   	f.write("\tdcterms:creator "+full_authors+";\n")
	   	f.write("\tfrbr:realization adage:"+ref_id+"Expression.\n")
	   	f.write("adage:"+ref_id+"Expression a fabio:Expression;\n")
	   	f.write('\tdcterms:title "'+paper_name+'";\n')
	   	f.write('\tfabio:hasPublicationYear "'+year+'"^^xsd:gYear.\n\n')
	   	for e in split_author_id:
	   		for line in c3:
	   			if (line[0]==e):
	   				f.write("adage:"+e+" a foaf:Person ;\n")
	   				f.write('\tfoaf:givenName "'+line[1]+'";\n')
	   				f.write('\tfoaf:familyName "'+line[2]+'".\n')
	   				f.write("\n\n")
	   		f3.seek(1)
	   		

	   	
	   	
	   	f.close()
	   		

	    
	   else:
	   	count+=1

	   
	   