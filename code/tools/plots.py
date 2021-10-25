### A class for handling the plots.



import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context('talk')
import missingno as msno
import numpy as np

from matplotlib.lines import Line2D



IMAGE_PATH = '../presentation/images'
IMAGE_PATH_MAPS = f'{IMAGE_PATH}/maps'
IMAGE_PATH_GRAPHS = f'{IMAGE_PATH}/graphs'
IMAGE_PATH_DEGREES = f'{IMAGE_PATH}/degrees'
IMAGE_PATH_NULL = f'{IMAGE_PATH}/null'

class PlotH:
  def __init__(self):
    self.title_fontsize = 24
    self.suptitle_fontsize = 26
    self.legend_fontsize=24


  def round_large_num(self, num):
    """
    A helper method to display large numbers.
    """
    if num > 1000:
      r = int(np.log10(num))-1
      return round(num, -r)
    return num

  def color_labels_by_source_target(self,g, s_col='b', t_col='g', lw=2):
    """
    Color the lables by source/target
    """
    labels = g.get_xticklabels()
    custom_lines = [Line2D([0], [0], color=s_col, lw=lw),
                    Line2D([0], [0], color=t_col, lw=lw)]
    legend_text = ['Source', 'Target']
    for label in labels:
      t = label.get_text()
      if t.endswith('_s') or t.startswith('START_'):
        label.set_color(s_col)
      elif t.endswith('_t') or t.startswith('END_'):
        label.set_color(t_col)
    return custom_lines, legend_text

  def get_missing_info(self, df, name, conversions={}):
      """
      Extract the missing information corresponding to the given table.
      """
      null_df = df.copy()
      null_df = null_df.rename(columns = conversions)
      s = null_df.isnull().sum().sum()
      null_ratio = (s/df.size)*100
      null_ratio_str = f'{null_ratio:.0f}%' if null_ratio > 1 else f'{null_ratio:.3f}%'
      # title_str =  f'shape: ({df.shape[0]:,}|{df.shape[1]})\nnull ratio: {null_ratio_str}'
      nrow = self.round_large_num(df.shape[0])
      title_str =  f'shape: ({nrow:,}|{df.shape[1]})\nnull ratio: {null_ratio_str}'
      return null_df, title_str

  def plot_missing_values(self, df, name, conversions={}, figsize = (8, 3), is_clean=True, 
                          bbox_to_anchor=(0, -.05),
                          method='matrix', extra='', to_sort=False, change_colors=False, title=''):
      """
      Method for plotting values of missing values.
      """
      null_df, title_str = self.get_missing_info(df, name, conversions=conversions)

      if to_sort:
        null_df = msno.nullity_sort(null_df, sort='descending')

      if method == 'matrix':
        g = msno.matrix(null_df, figsize=figsize, sparkline=False); 
      else:
        g = msno.dendrogram(null_df, figsize=figsize, orientation='top');

      g.set(yticklabels=[])
      if change_colors:
        custom_lines, legend_text = self.color_labels_by_source_target(g)
        plt.legend(custom_lines, legend_text, 
                  bbox_to_anchor=bbox_to_anchor, ncol=2,
                   loc='upper left', frameon=False, fontsize=self.legend_fontsize)

      name_to_show = name.replace('_', ' ')
      default_title = f'Table: "{name_to_show}"'
      use_title = title if title!='' else default_title
      plt.title(f'{use_title}\n{title_str}', fontsize=self.title_fontsize)
      modname = name.replace(' of', '').replace('/', '_').replace(' ', '_').replace('__', '_')
      fname = f'{IMAGE_PATH_NULL}/{method}_{modname}_{"clean" if is_clean else "orig"}_{extra}.png'
      plt.savefig(fname, bbox_inches='tight', dpi=300)


  def plot_missing_data_orig_clean(self, df_orig, df_clean, name, conversions={}, figsize = (20, 3), method='matrix'):
    """
    Plot missing data for a given method of showing null values
    """
    fig, axs = plt.subplots(1, 2, figsize=figsize)
    null_df_orig, title_str_orig = self.get_missing_info(df_orig, name, conversions=conversions)
    null_df_clean, title_str_clean = self.get_missing_info(df_clean, name, conversions=conversions)


    s_null_df_orig = msno.nullity_sort(null_df_orig, sort='descending')
    if method == 'matrix':
      g0 = msno.matrix(s_null_df_orig, ax=axs[0], sparkline=False); 
    else:
      g0 = msno.dendrogram(s_null_df_orig, orientation='top', ax=axs[0]); 

    g0.set(yticklabels=[])
    g0.set_title(title_str_orig)

    s_null_df_clean = msno.nullity_sort(null_df_clean, sort='descending')

    if method == 'matrix':
      g1 = msno.matrix(s_null_df_clean, ax=axs[1], sparkline=False); 
    else:
      g1 = msno.dendrogram(s_null_df_clean, orientation='top', ax=axs[1]); 
    g1.set(yticklabels=[])
    g1.set_title(title_str_clean)


    name_to_show = name.replace('_', '\n')
    plt.suptitle(f'{name_to_show}', fontsize=self.suptitle_fontsize)
    fname = f'{IMAGE_PATH_NULL}/missing_{method}_{name}_orig_clean.png'
    plt.savefig(fname, bbox_inches='tight', dpi=300)


  def plot_edge_types_bar_chart(self, edges_info, figsize=(10, 15), count=25):
    """
    Make a bar chart for displaying the count of links.
    """
    links = edges_info['link'].value_counts().index.tolist()
    total = len(links)
    title = f'Edge Types\n{count} of {total}'
    plt.figure(figsize=figsize)
    g = sns.countplot(data=edges_info, y='link',alpha=.5,
                order = edges_info['link'].value_counts().head(count).index);
    g.set_title('Edge Types')
    g.set_ylabel('')
    g.set_xscale('log')
    g.tick_params(left=False)
    sns.despine()
    fname = f'{IMAGE_PATH}/edges/edge_types_bar_chart_{count}_{total}.png'
    plt.savefig(fname, bbox_inches='tight', dpi=300)

  def plot_categorical_heatmap(self, dataframe, ncat=50, cols_to_remove=[], cmap='tab20c',
                               sort_by=[], figsize=(25, 10), title='', return_df=False):
    """
    A method for showing the categorical data in a similar look to missingno.
    Got help from 
    https://stackoverflow.com/questions/61097853/seaborn-heatmap-adjust-linewidth-for-vertical-and-horizontal-line-separately
    for adjusting the heatmap.
    """

    sort_by_str = ''
    if sort_by:
      sort_by_str = 'sort_'+ '_'.join(sort_by)
    columns_to_pick = dataframe.columns
    if ncat!=0:
      columns_to_pick = dataframe.nunique()[dataframe.nunique()<ncat].index.tolist()

    cols = [c for c in columns_to_pick if c not in cols_to_remove]
    df = dataframe[cols].copy()#.sample(100)
    mask = np.zeros_like(df)
    df_is_null = df.isnull()
    mask[df_is_null] = True
    nrows = f'e{int(np.log10(df.shape[0]))}'
    df = df.astype(str)
    hmdf = df.stack(dropna=False).rank(method='dense').unstack(fill_value=np.nan)
    hmdf = hmdf.mask(df_is_null)

    if not sort_by:
      sort_by = hmdf.nunique().sort_values().index.tolist()
    hmdf.sort_values(by=sort_by, inplace=True)

    plt.figure(figsize=figsize)

    hmdf = (hmdf-hmdf.mean())/(hmdf.max()-hmdf.min())


    with sns.axes_style("white"):
      g = sns.heatmap(hmdf, cbar=False,mask=mask, cmap=cmap, yticklabels=False)
      g.xaxis.set_ticks_position("top")
      g.set_xticklabels(g.get_xticklabels(),rotation = 70);
      g.set_xlabel('');
      # g.set_yticklabels([])
      g.tick_params(left=False, top=False)
      title_str = title.title()+' Columns'
      g.set_title(title_str, fontsize=self.title_fontsize)


      for i in range(hmdf.shape[1]+1):
        g.axvline(i, color='white', lw=2)
      fpath = f'{IMAGE_PATH}/edges/heatmap_{title}_{sort_by_str}_n{ncat}_r{nrows}_c{cmap}.png'
      plt.savefig(fpath, bbox_inches='tight', dpi=300)
    if return_df:
      return hmdf