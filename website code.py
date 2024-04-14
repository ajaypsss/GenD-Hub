from nicegui import ui
import pandas as pd
from io import BytesIO
from PIL import Image
import sqlite3
import math
con=sqlite3.connect("E:/Disease.db")
cur=con.cursor()

@ui.page('/disorder/{aj}')
def acro(aj: int):
    ui.query('body').classes('bg-gradient-to-t to-sky-50 from-sky-100')
    global clinvar
    global list1
    clinvar=(cur.execute("  select * from xclinvar2 l where l.new==?",(aj,))).fetchall()
    
    defin=(cur.execute("select * from alldef d where d.new==?",(aj,))).fetchall()

    syno=(cur.execute("select l.synonyms from dissyn l where l.new==?",(aj,))).fetchall()

    list1=(cur.execute("select * from list1 where list1.new==?",(aj,))).fetchone()

    genes=(cur.execute("select * from gene1 g where g.new==?",(aj,))).fetchall()

    prev=(cur.execute("select p.loc,p.prevalance,p.link from prev4 p where p.new==?",(aj,))).fetchall()

    epi=(cur.execute("  select l.age,l.inheritance from ageinher l where l.new==?",(aj,))).fetchone()

    links=(cur.execute("  select * from dislinks l where l.new==?",(aj,))).fetchall()

    ajphen=(cur.execute("  select l.hpid,l.freq from ajphen l where l.new==?",(aj,))).fetchall()


    with ui.splitter(horizontal=False, value=75).classes('w-full h-screen') as split:
        with split.before:
            with ui.card().classes('w-full h-10 no-shadow bg-sky-50'):
                ui.label()
            
            #for the disease name and the aj id
            with ui.card().tight().classes('fixed no-shadow bg-sky-50 w-2/3 z-20'):
                with ui.row():

                    ui.label(list1[6]).classes(' text-cyan-950 font-sans text-bold text-2xl ml-10')#disease name
                    ui.label(f'[ {list1[0]} ]').classes('text-cyan-900 font-sans text-semibold text-2xl ml-15')#disease id
            
            with ui.row().classes('ml-10 font-sans text-cyan-900 '):
                ui.label(list1[1])
                ui.label(list1[2])
                ui.label(list1[3])
                ui.label(list1[4])

            #disease synonyms
            with ui.card().tight().classes('w-4/5 p-2 ml-10 bg-sky-50  text-cyan-900/75 '):
                ui.label('Synonyms').classes('font-sansml-2 mb-3 text-bold text-lg break-all')
                #with ui.row():
                for sy in syno:
                    with ui.row():
                        ui.icon('navigate_next').classes('mt-1')
                        ui.label(sy).classes('mb-0 break-all')
                        
            #DIsorder descriptions
            with ui.card().tight().classes('w-4/5 p-1 ml-10 mt-5 bg-sky-50 text-cyan-900/75'):
                
                ui.label('Disorder Description').classes('font-sans ml-2  text-bold text-lg')
                if defin:
                    with ui.row():
                        ui.label('( From sources:').classes('font-sans ml-2 mb-3 text-medium text-sm') 
                        for defi in defin:
                            ui.label(f'{defi[2]} ').classes('font-sans ml-2 mb-3 text-medium text-sm')
                        ui.label(')') 
                    
                    k=['a','b','c','d','e'];variable=-1
                    with ui.tabs() as tabs:
                        for di in defin:
                            variable+=1
                            ui.tab(k[variable], label=di[2]).classes('px-5 rounded-t-lg font-sans text-cyan-800 bg-sky-200 transition ease-in-out delay-200 hover:scale-110 hover:text-cyan-950 duration-300')

                    with ui.tab_panels(tabs, value=k[0]).classes('w-full'):
                        variable=-1
                        for di in defin:
                            variable+=1
                            with ui.tab_panel(k[variable]).classes('p-0'):
                                
                                with ui.scroll_area().classes(' text-justify font-sans text-cyan-900 border bg-sky-100  hover:text-slate-950'):
                                    ui.html(di[0])
                else:
                    ui.label(" Not available").classes('text-lg font-sans ml-2')

            #epidemiology data
            with ui.card().tight().classes('w-4/5 p-1 ml-10 mt-5 bg-sky-50 text-cyan-900/75 font-sans'):
                ui.label('Disorder Epidemiology').classes('font-sans ml-2 mb-2 text-bold text-lg')


                with ui.row():
                    ui.label('Type of inheritance:').classes('text-base font-medium ml-2')
                    if epi:
                        ui.label(epi[1]).classes('text-base font-normal')
                    else:
                        ui.label("Not Available")

                with ui.row():
                    ui.label('Age of Onset:').classes('text-base font-medium ml-2')
                    if epi:
                        ui.label(epi[0]).classes('text-base font-normal')
                    else:
                        ui.label("Not Available")


                col=[{'name': 'name', 'label': 'Region', 'field': 'name', 'align': 'left'},
                     {'name': 'link', 'label': 'Prevalance', 'field': 'link', 'align': 'left'},
                     {'name': 'alink', 'label': 'Resources supporting the data', 'field': 'alink', 'align': 'left'}]
                
                df=pd.DataFrame(prev,columns=[c['name'] for c in col])
                tabl=ui.table(columns=col, rows=df.to_dict(orient='records'), title='Disorder Prevalance Data').classes('bg-sky-100 table-auto font-sans p-0  mt-2')
                tabl.add_slot('body-cell-alink', '''
                    <q-td :props="props">
                        <a :href="props.value">{{ props.value }}</a>
                    </q-td>
                ''')

            #related gene data
            #associated gene
            with ui.card().tight().classes('w-4/5 p-1 ml-10 mt-5 bg-sky-50 text-cyan-900/75 h-96'):
                ui.label(f'Associated Genes - {len(genes)}').classes('font-sans ml-2 mb-2 text-bold text-lg')

                with ui.scroll_area().classes('h-80'):
                    for gene in genes:
                        genedetails=(cur.execute("select gd.GeneID,gd.chromosome,gd.map_location,gd.description,gd.type_of_gene from genedetails1 gd where gd.GeneID==?",(gene[3],))).fetchone()
                        #with ui.expansion(f'{gene[1]}  [ GeneID:   {genedetails[0]} ]',icon='label').classes('w-full rounded-xl bg-sky-100 font-medium font-sans hover:text-cyan-900 hover:bg-sky-200 '):
                        with ui.expansion().classes('w-full font-sans font-medium bg-sky-100 rounded-xl hover:rounded-lg hover:text-cyan-900 hover:bg-sky-200') as expan:
                            with expan.add_slot('header'):
                                with ui.column():
                                    with ui.row():
                                        ui.label(f'{gene[0]}').classes('text-bold')
                                        if genedetails:

                                            ui.label('-')
                                            ui.label(genedetails[3]).classes('text-bold')#gene name
                                    if genedetails:
                                        ui.label(f'Gene ID : {genedetails[0]}')
                            
                            blob=(cur.execute("select * from ideogram1 i where i.geneid==?",(gene[3],))).fetchone()
                            image=Image.open(BytesIO(blob[1]))
                            
                            ui.image(image).classes('w-full')# object-left p-0 m-0 hover:object-fill
                            if genedetails:
                                ui.label(f'Chromosome: {genedetails[1]}')

                                ui.label(f'Type of gene : {genedetails[4]}')
                                
                            else:
                                ui.label("Remaining data to be updated soon...")

                            ui.label(f'Gene Score *: {gene[1]}/4').classes('text-sm')#something smalller than small
                            ui.label()
                            ui.link(f'View {gene[0]} in Genome Data Viewer',f'https://www.ncbi.nlm.nih.gov/genome/gdv/browser/gene/?id={genedetails[0]}',new_tab=True)

                            ui.link(f'More on {gene[0]}',f'/gene/{genedetails[0]}',new_tab=True)#need to create a page for that
                            ui.label()

                            ui.label("*Gene Score- the reliability of gene with the disease on a scale of 4").classes('text-xs italic font-normal ')

                ui.label("*Genes are arranged in the decreasing order of their association with the disease").classes('text-xs')

            #related phenotype data           
            with ui.card().tight().classes('w-4/5 p-1 ml-10 mt-5 bg-sky-50 text-cyan-900/75'):
                if len(ajphen)>0:
                    ui.label(f'Associated Phenotypes - {len(ajphen)}').classes('font-sans ml-2 mb-2 text-bold text-lg')

                    with ui.scroll_area().classes():
                        #ui.label(ajphen)
                        for phen in ajphen:
                            phendef=(cur.execute("select * from phendef l where l.hp==?",(phen[0],))).fetchone()

                            with ui.expansion().classes('w-full font-sans font-medium bg-sky-100 rounded-xl hover:rounded-lg hover:text-cyan-900 hover:bg-sky-200') as expan:
                                with expan.add_slot('header'):
                                    with ui.column():
                                        with ui.row():
                                            ui.label(f'{phen[0]}').classes('text-bold')
                                            if  phendef:
                                               
                                                ui.label(f'{phendef[2]}').classes('text-bold')#name

                                        if phen[1]:
                                            ui.label(f'Frequency: {phen[1]}')
                                if phendef:
                                    ui.label(phendef[3]).classes()
                                    ui.label(f'(Source: {phendef[4]})').classes('text-xs font-normal')#something smalller than small

                                else:
                                    ui.label("Data to be updated soon...")
                else:
                    ui.label(f'Associated Phenotypes - Not Available in the database').classes('font-sans ml-2 mb-2 text-bold text-lg')

            #variations from clinvar
            with ui.card().tight().classes('w-4/5  p-1 ml-10 mt-5 bg-sky-50 text-cyan-900/75 '):
                #height of the card is not customizable here
                ui.label(f'Variations - {len(clinvar)}').classes('font-sans ml-2 mb-2 text-bold text-lg')
                if len(clinvar)!=0:
                    with ui.row():
                        ui.label("For detailed access to variation information, ").classes('ml-5')
                        ui.link('Click here',f'/disorder/{aj}/variations',new_tab=True)
                    with ui.scroll_area().classes('h-screen'):#.classes('p-0 text-justify text-zinc-900 border bg-slate-300  hover:text-slate-950'):
                        
                        x=0
                        for dis in clinvar:
                            x+=1
                            if x>15:
                                break
                            
                            #with ui.expansion(f'{dis[17]} \n- [type: {dis[21]}]', icon='label').classes('rounded-xl hover:rounded-lg w-full font-medium  font-sans bg-sky-100 hover:text-cyan-900 hover:bg-sky-200 text-center '):
                            with ui.expansion().classes('w-full font-sans font-medium bg-sky-100 rounded-xl hover:rounded-lg hover:text-cyan-900 hover:bg-sky-200') as expan:
                                with expan.add_slot('header'):
                                    with ui.column():
                                        ui.label(f'{dis[17]}').classes('text-bold')
                                        ui.label(f'Vaiation Type: {dis[21]}')
                                ui.label(f'Alternate names: {dis[18]}')
                                ui.label(f'SPDI: {dis[3]}')
                                ui.label(f'Gene(s): {dis[24]}')
                                ui.label(f'Cytogenic location: {dis[23]}')
                                ui.label(f'Molecular consequence: {dis[22]}')
                                with ui.row():

                                    ui.label(f'PubMed references for this variation: ')
                                    ui.link(f'[{dis[2]}]',f'{dis[1]}',new_tab=True)
                                ui.label('Genomic location:')
                                with ui.row():
                                    ui.link('GRCh38',f'{dis[15]}',new_tab=True)
                                    ui.link('UCSC',f'{dis[13]}',new_tab=True)
                                with ui.row():
                                    ui.link('GRCh37',f'{dis[16]}',new_tab=True)
                                    ui.link('UCSC',f'{dis[14]}',new_tab=True)
                                ui.label("More Information:")
                                if dis[10]:
                                    with ui.row():
                                        ui.label('Clinvar:')
                                        ui.link(f'{dis[10]}',f'{dis[11]}',new_tab=True)
                                if dis[4]:
                                    with ui.row():
                                        ui.label('OMIM:')
                                        ui.link(f'{dis[4]}',f'{dis[5]}',new_tab=True)
                                if dis[6]:
                                    with ui.row():
                                        ui.label('dbSNP:')
                                        ui.link(f'rs{dis[6]}',f'{dis[7]}',new_tab=True)
                                if dis[8]:
                                    with ui.row():
                                        ui.label('ClinGen:')
                                        ui.link(f'{dis[8]}',f'{dis[9]}',new_tab=True)
            ui.label('May be the END...')
        
        with split.after:
            
            with ui.card().tight().classes('object-center ml-10 mt-10 p-3'):
                ui.label('Genetic Disorder Hub (GenD HUB)').classes('text-lg font-sans ')
                disorders=[]
                diso=(cur.execute("select l.input from dissyn l")).fetchall()
                for disor in diso:
                    disorders.append(disor)

                k=ui.select(options=disorders,with_input=True,
                            on_change=lambda e:inhere(e)).classes('w-full')

            with ui.card().classes('w-full h-10 no-shadow bg-sky-50 pl-10 font-sans text-cyan-900'):
                ui.label("For more disorder related information:")
            
                for lin in links:
                    if lin[1]:
                        with ui.row():
                            ui.icon('arrow_right').classes('mt-1')
                            ui.link('OMIM',lin[1],new_tab=True)
                    if lin[2]:
                        with ui.row():
                            ui.icon('arrow_right').classes('mt-1')
                            ui.link('Orphanet',lin[2],new_tab=True)
                    if lin[3]:
                        with ui.row():
                            ui.icon('arrow_right').classes('mt-1')
                            ui.link('MedlinePlus',lin[3],new_tab=True)
                    if lin[4]:
                        with ui.row():
                            ui.icon('arrow_right').classes('mt-1')
                            ui.link('DisGeNET',lin[4],new_tab=True)
