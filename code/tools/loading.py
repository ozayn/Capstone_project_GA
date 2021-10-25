
### A class for handling loading and writing the data.


import os
import pandas as pd

DATA_PATH = '../data'
ORIGINAL_DATA_PATH = f'{DATA_PATH}/original/csv_offshore_leaks'
CLEAN_DATA_PATH = f'{DATA_PATH}/clean'


class DataH:
  def __init__(self):
    pass

  def read_dataframes(self, paths):
    data_frames = {}
    for name, path in paths.items():
      data_frames[name] = pd.read_csv(path)
    return data_frames

  def get_original_file_paths(self, ext='.csv'):
    file_names = os.listdir(ORIGINAL_DATA_PATH)
    return {f"{'_'.join(n.split('.')[1:-1])}": f'{ORIGINAL_DATA_PATH}/{n}' 
            for n in file_names
            if n.endswith(ext)} 

  def get_clean_file_paths(self, ext='.csv'):
    file_names = os.listdir(CLEAN_DATA_PATH)
    return {f"{n.split('.')[0]}": f'{CLEAN_DATA_PATH}/{n}' 
            for n in file_names if n.endswith(ext)} 


  def read_original_dataframes(self):
    paths = self.get_original_file_paths()
    return self.read_dataframes(paths)

  def read_clean_dataframes(self):
    paths = self.get_clean_file_paths()
    return self.read_dataframes(paths)


  def get_common_between_lists(self, lists):
    common = set(lists[0])
    for l in lists[1:]:
      common = common.intersection(l)
    return list(common)


  def print_unique_items(self, df):
    to_drop = []
    nunique = df.nunique().to_dict()
    for k, v in nunique.items():
      if v<=1:
        to_drop.append(k)
      if v == 1:
        print(f'\n\tThere is {v} value for "{k}":\n\t\t{df.head(1)[k].values[0]}')
      elif v < 5:
        print(f'\n\tThere are {v} values for "{k}"')
        for value in df[k].unique().tolist():
          print(f'\t\t{value}')
    if len(to_drop)>0:
      print('\n\tdrop ', to_drop)
    return to_drop


  def write_clean_data_frames(self):

    given_to_drop = {'edges': ['TYPE'], 'nodes_entity': ['note']}
    data_frames = self.read_original_dataframes()
    to_drop_dict = {}
    for name, df in data_frames.items():
      print(f'\n\n{name}:')
      to_drop = self.print_unique_items(df)
      to_drop_dict.update({name: to_drop})


    common_to_drop_columns = self.get_common_between_lists(list(to_drop_dict.values()))


    clean_data_frames = {}
    for name, df in data_frames.items():
      df_new = df.copy().drop(columns=to_drop_dict[name]+given_to_drop.get(name, []))
      df_new.drop_duplicates(inplace = True)
      if 'node_id' in df_new.columns:
        if df_new['node_id'].isnull().sum()>0:
          display(df_new['node_id'].isnull().sum())
      clean_data_frames.update({name: df_new})

    for name, df in clean_data_frames.items():
      print(f'\n\n{name}:')
      self.print_unique_items(df)

      if 'jurisdiction' in df.columns:
        null_j = df['jurisdiction_description'] == 'Undetermined'
        df.loc[null_j , 'jurisdiction'] = None
        df.loc[null_j , 'jurisdiction_description'] = None
        df.loc[df['jurisdiction_description']=='Recorded in leaked files as "fund"', 'jurisdiction_description'] = 'Recorded as fund'

      if 'country_codes' in df.columns:
        no_location_rows = df['country_codes']=='XXX'
        df.loc[no_location_rows, 'country_codes'] = None
        df.loc[no_location_rows, 'countries'] = None
      if name == 'edges':
        df['start_date'] = pd.to_datetime(df['start_date'])
        df['end_date'] = pd.to_datetime(df['end_date'])

      if 'incorporation_date' in df.columns:
        df['incorporation_date'] = pd.to_datetime(df['incorporation_date'])
      df.to_csv(f'{CLEAN_DATA_PATH}/{name}.csv', index=False)