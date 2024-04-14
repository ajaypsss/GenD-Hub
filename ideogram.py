#this is the oneeeeeeeeeeee with chromosomal location added properly size 16
#!/usr/bin/env python
import sqlite3
connect= sqlite3.connect('E:/newdis2811idx.db')  # Replace 'your_database.db' with your actual database file
curs=connect.cursor()


"""
 plotting chromosome ideograms and genes using matplotlib.

1) Assumes a file from UCSC's Table Browser from the "cytoBandIdeo" table,
saved as "ideogram.txt". Lines look like this::

    #chrom  chromStart  chromEnd  name    gieStain
    chr1    0           2300000   p36.33  gneg
    chr1    2300000     5300000   p36.32  gpos25
    chr1    5300000     7100000   p36.31  gneg

2) Assumes another file, "ucsc_genes.csv" that contains gene region informations.

"""

from matplotlib import pyplot as plt
from matplotlib.collections import BrokenBarHCollection
import pandas
from io import BytesIO


#function that we'll call for each dataframe (once for chromosome
# ideograms, once for genes).  The rest of this script will be prepping data
# for input to this function
#
def chromosome_collections(df, y_positions, height,  **kwargs):
    del_width = False
    if 'width' not in df.columns:
        del_width = True
        df['width'] = df['end'] - df['start']
    for chrom, group in df.groupby('chrom'):
        
        yrange = (y_positions[chrom], height)
        xranges = group[['start', 'width']].values
        yield BrokenBarHCollection(
            xranges, yrange, facecolors=group['colors'], **kwargs)
    if del_width:
        del df['width']

def chrom(chromosome,generow):
    # Height of each ideogram
    chrom_height = 1
    # Spacing between consecutive ideograms
    chrom_spacing = 1
    # Height of the gene track. Should be smaller than `chrom_spacing` in order to
    # fit correctly
    gene_height = 1
    # Padding between the top of a gene track and its corresponding ideogram
    gene_padding = 0
    # Width, height (in inches)
    figsize = (15, 1)
    # Decide which chromosomes to use
    if chromosome=='chr1':
        chromosome_list = ['chr3',chromosome]# when running automated here the chromsome no og the gene should be updated
    else:
        chromosome_list = ['chr1',chromosome]# when running automated here the chromsome no og the gene should be updated

    # Keep track of the y positions for ideograms and genes for each chromosome,
    # and the center of each ideogram (which is where we'll put the ytick labels)
    ybase = 0
    chrom_ybase = {}
    gene_ybase = {}
    chrom_centers = {}

    # Iterate in reverse so that items in the beginning of `chromosome_list` will
    # appear at the top of the plot
    for chrom in chromosome_list[::-1]:
        chrom_ybase[chrom] = ybase
        chrom_centers[chrom] = ybase + chrom_height / 2.
        gene_ybase[chrom] = ybase - gene_height - gene_padding
        ybase += chrom_height + chrom_spacing

    # Read in ideogram.txt, downloaded from UCSC Table Browser use that file accordingly in the E: folder
    ideo = pandas.read_table(
        'E:/cytoBandIdeo.txt',
        skiprows=1,
        names=['chrom', 'start', 'end', 'name', 'gieStain']
    )

    # Filter out chromosomes not in our list
    ideo = ideo[ideo.chrom.apply(lambda x: x in chromosome_list)]

    # Add a new column for width
    ideo['width'] = ideo.end - ideo.start

    # Colors for different chromosome stains
    color_lookup = {
        'gneg': (1., 1., 1.),
        'gpos25': (.6, .6, .6),
        'gpos50': (.4, .4, .4),
        'gpos75': (.2, .2, .2),
        'gpos100': (0., 0., 0.),
        'acen': (.8, .4, .4),
        'gvar': (.8, .8, .8),
        'stalk': (.9, .9, .9),
    }

    # Add a new column for colors
    ideo['colors'] = ideo['gieStain'].apply(lambda x: color_lookup[x])
    # Same thing for genes
    genes=pandas.DataFrame([generow],columns=['index','chrom', 'start', 'end', 'map','geneid','gene'])
    genes = genes[genes.chrom.apply(lambda x: x in chromosome_list)]
    if (generow[3]-generow[2])<400000:
        genes['width'] =(generow[3]-generow[2] )+400000
        #diff= generow[3]-generow[2]+400000#for checking

    else:
        genes['width'] =generow[3]-generow[2]
        #diff= generow[3]-generow[2]#for checking
    
    genes['colors'] = '#FF0000'

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111,frameon=False)#frameon to remove the border from the graph
    fig.patch.set_visible(False) #i added this, thus the white backgroung arounthe ideogram gone


    # Now all we have to do is call our function for the ideogram data...
    for collection in chromosome_collections(ideo, chrom_ybase, chrom_height):
        ax.add_collection(collection)
    # ...and the gene data
    for collection in chromosome_collections(
        genes, gene_ybase, gene_height, alpha=1, linewidths=1
    ):
        ax.add_collection(collection)

    ax.axis('tight')
    ax.set_yticks([])
    ax.set_xticks([])

    from matplotlib.pyplot import savefig
    max_y = plt.gca().get_ylim()[1]
    plt.ylim(max_y/2 ,-0.7) 
    plt.subplots_adjust(bottom=0.35)
    #fontsize=18
    plt.xlabel(f'Chromosomal location of {generow[6]} : {generow[4]}',fontsize=16)
    buf = BytesIO()
    plt.savefig(buf,format='png')
    buf.seek(0)
    curs.execute('INSERT INTO ideogram1 (geneid,ideogram,map) VALUES (?,?,?)', (generow[5],buf.read(),generow[4]))
    connect.commit()
hi1=pandas.read_csv("E:/ucscgenes1.csv")
#hi1=hi.head(5)
for gene in hi1.itertuples():
    if gene[2] and gene[3]:
        chrom(gene[1],gene)
        