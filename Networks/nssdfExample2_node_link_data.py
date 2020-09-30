{'directed': True,
 'multigraph': False,
 'graph': {'name': 'NSSDF 2009 Example 2',
           'algebra': 'Extended_Linear_Interval_Algebra',
           'description': 'Using Semantic Web Technology to Exploit Soft Information'
           },
 'nodes': [{'classes': ['ProperInterval'], 'id': 'Yesterday'},
           {'classes': ['ProperInterval'], 'id': 'Today'},
           {'classes': ['ProperInterval'], 'id': 'Yesterday_Morning'},
           {'classes': ['ProperInterval'], 'id': 'Yesterday_Evening'},
           {'classes': ['Point'], 'id': 'Time_of_Obs'},
           {'classes': ['Point'], 'id': 'Time_of_Arrest'},
           {'classes': ['Point'], 'id': 'Time_of_Release'},
           {'classes': ['ProperInterval', 'Point'], 'id': 'Period_of_Detention'}
           ],
 'links': [{'constraints': 'M', 'source': 'Yesterday', 'target': 'Today'},
           {'constraints': 'SI', 'source': 'Yesterday', 'target': 'Yesterday_Morning'},
           {'constraints': 'FI', 'source': 'Yesterday', 'target': 'Yesterday_Evening'},
           {'constraints': 'DI', 'source': 'Today', 'target': 'Time_of_Release'},
           {'constraints': 'B', 'source': 'Yesterday_Morning', 'target': 'Yesterday_Evening'},
           {'constraints': 'DI', 'source': 'Yesterday_Morning', 'target': 'Time_of_Arrest'},
           {'constraints': 'DI', 'source': 'Yesterday_Evening', 'target': 'Time_of_Obs'},
           {'constraints': 'PS', 'source': 'Time_of_Arrest', 'target': 'Period_of_Detention'},
           {'constraints': 'PF', 'source': 'Time_of_Release', 'target': 'Period_of_Detention'}
           ]
 }
