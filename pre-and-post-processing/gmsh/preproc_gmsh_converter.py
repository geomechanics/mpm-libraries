# --- IMPORT LIBRARIES ---
import pandas as pd
import os
import shutil

# --- USER INPUTS ---
#in_dir: directory of .csv file to be converted
in_dir = '/home/ledt/mpm-libraries/pre-and-post-processing/gmsh/example-files/'
#ori_file: name of .csv file to be converted (must be comma-delimited .csv)
#convert .msh to .csv before using this tool
ori_file = 'to_convert.csv'
#mesh_flag: if true, will output mesh.txt file
mesh_flag = True
#entity_sets_flag: if true, will output entity_sets.json files for each surface
#setup for bounding box only
entity_sets_flag = True
#velocity_constraints_flag: if true, will output velocity_constrains.txt file
#setup for bounding box only; does not consider duplicates/conflicts on edges
velocity_constraints_flag = True
#velocity constraints: insert desired values per direction; X=0, Y=1, Z=2
#() for no BC on that bounding box surface; None for no BC in that direction
Surface_Zmin = (0, 0, 0)
Surface_Ymin = (0, 0, 0)
Surface_Xmax = (None, None, None)
Surface_Ymax = (None, None, None)
Surface_Xmin = (None, None, None)
Surface_Zmax = (None, None, None)


# --------------------------------------------------------------------
def gmsh_converter_tet(in_dir,
                       ori_file,
                       mesh_flag,
                       entity_sets_flag,
                       velocity_constraints_flag,
                       Surface_Zmin=pd.DataFrame(),
                       Surface_Ymin=pd.DataFrame(),
                       Surface_Xmax=pd.DataFrame(),
                       Surface_Ymax=pd.DataFrame(),
                       Surface_Xmin=pd.DataFrame(),
                       Surface_Zmax=pd.DataFrame()):

    # --- 0. USER INPUTS (CUSTOMIZATIONS) ---
    #mesh_file: name of converted mesh.txt
    mesh_file = 'mesh.txt'
    #velocity_constraints_file: name of converted velocity_constraints.txt
    velocity_constraints_file = 'velocity_constraints.txt'
    #entity_sets_file: name of converted entity_sets file WITHOUT suffix
    #will make a .json file
    entity_sets_file = 'entity_sets'
    #temp_space: name of temporary calculation space for conversion
    temp_space = 'temp_conversion_space_tet/'
    #nodes_file: name of temporary .csv to store all node information
    nodes_file = 'nodes_all.csv'
    #elements_file: name of temporary .csv to store all element information
    elements_file = 'elements_all.csv'
    #dflag: if true, will delete files/folders if already exist
    dflag = True
    #Surface_tags: dictionary of tags associated with each bounding box surface
    #tag numbers defined in gmsh input file
    Surface_tags = {
        13: Surface_Zmin,
        14: Surface_Ymin,
        15: Surface_Xmax,
        16: Surface_Ymax,
        17: Surface_Xmin,
        18: Surface_Zmax
    }

    # --- 1. SETUP ---
    # - 1.1 Directory setup -
    in_dir1 = in_dir
    in_dir2 = os.path.join(in_dir1, temp_space)
    try:
        os.mkdir(in_dir1 + temp_space)
    except FileExistsError:
        if dflag == True:
            shutil.rmtree(in_dir1 + temp_space)
            os.mkdir(in_dir1 + temp_space)
            print("Directory '%s' overwritten" % in_dir2)
        else:
            print("Directory '%s' already exists... quitting" % in_dir2)
            quit()

    # - 1.2 Read the csv file -
    df = pd.read_csv(in_dir1 + ori_file, header=None)

    # - 1.3 Create working conversion files and read their dataframes -
    shutil.copyfile(in_dir1 + ori_file, in_dir2 + nodes_file)
    shutil.copyfile(in_dir1 + ori_file, in_dir2 + elements_file)
    df_n = pd.read_csv(in_dir2 + nodes_file, header=None)
    df_e = pd.read_csv(in_dir2 + elements_file, header=None)

    # - 1.4 Locate division between nodes and elements -
    Nlist = df.index[df[0] == '$EndNodes'].tolist()
    N = Nlist[0]

    # --- 2.0 NODES ---
    #find start and end of nodes in gmsh file
    Mlist = df.index[df[0] == '$Nodes'].tolist()
    Mn = Mlist[0] + 2
    Nn = N
    #slice to get only nodes, calculate number of nodes
    df_n = df_n.iloc[Mn:Nn, :]
    nnodes = df_n.shape[0]
    #correct node indices to start from 0
    df_n[0] = df_n[0].apply(lambda x: int(x) - 1)
    #export to .csv nodes_file
    df_n.to_csv(in_dir2 + nodes_file, index=False, header=False)

    # --- 3.0 ELEMENTS ---
    #find start and end of elements in gmsh file
    Mlist = df.index[df[0] == '$EndElements'].tolist()
    Me = Mlist[0]
    Ne = N + 3
    #slice to get only elements
    df_e = df_e.iloc[Ne:Me, :]
    #correct element indices to start from 0
    df_e[0] = df_e[0].apply(lambda x: int(x) - 1)
    for i in [5, 6, 7, 8]:
        df_e[i] = df_e[i].apply(lambda x: int(x) - 1 if pd.notnull(x) else x)
    #delete gmsh output column which provides no useful information
    del df_e[2]
    #export to .csv elements_file
    df_e.to_csv(in_dir2 + elements_file, index=False, header=False)

    # --- 4.0 MESH.TXT ---
    if mesh_flag == True:

        # - 4.1 Create & format parts -
        df_n_mesh = df_n
        #remove node indices column, reset headers
        del df_n_mesh[0]
        df_n_mesh.columns = range(df_n_mesh.columns.size)

        df_e_mesh = df_e
        #slice to get only volume elements, calculate number of volume elements
        df_e_mesh = df_e_mesh.loc[(df_e_mesh[3] == 19), [5, 6, 7, 8]]
        nelements_mesh = df_e_mesh.shape[0]
        #cast IDs to int then str (no trailing .0), reset headers
        df_e_mesh = df_e_mesh.astype(int).astype(str)
        df_e_mesh.columns = range(df_e_mesh.columns.size)

        #create header
        # yapf: disable
        df_mesh = pd.DataFrame([
            ['#!', 'elementShape', 'tetrahedron'],
            ['#!', 'elementNumPoints', 4],
            [str(nnodes), str(nelements_mesh), '']])
        # yapf: enable

        # - 4.2 Assemble parts & format -
        #assemble mesh.txt dataframe, remove extra trailing columns
        df_mesh = pd.concat([df_mesh, df_n_mesh, df_e_mesh],
                            axis=0,
                            ignore_index=True)
        df_mesh = df_mesh.drop(df_mesh.columns[[4, 5, 6, 7]], axis=1)

        # - 4.3 Export to .txt mesh_file -
        if not os.path.isfile(in_dir1 + mesh_file):
            df_mesh.to_csv(in_dir1 + mesh_file,
                           index=False,
                           header=False,
                           sep=' ')
        else:
            if dflag == True:
                os.remove(in_dir1 + mesh_file)
                df_mesh.to_csv(in_dir1 + mesh_file,
                               index=False,
                               header=False,
                               sep=' ')
                print("Mesh file '%s' overwritten" % mesh_file)
            else:
                print("Mesh file '%s' already exists... quitting" % mesh_file)
                quit()

    # --- 5.0 ENTITY_SETS.JSON ---
    if entity_sets_flag == True:
        # - 5.1 Create/reset/setup dataframes (outside loop) -
        df_entity_sets = pd.DataFrame()  #body
        #find location of start header, create footer
        first_tag = list(Surface_tags.keys())[0]
        # yapf: disable
        df_entity_sets_end = pd.DataFrame([
            ['', '', '', ']', '',],
            ['', '', '}', '', '',],
            ['', ']', '', '', '',],
            ['}', '', '', '', '',]]) #footer
        # yapf: enable

        # - 5.2 Create & format parts of surface dataframes (inside loop) -
        #loop through surfaces
        for tag in Surface_tags:
            df_tag = df_e
            #slice to get only elements on tagged surface
            df_tag = df_tag.loc[(df_tag[3] == tag), [5, 6, 7]]

            #create 1 column of all node indices for elements on tagged surface
            df_tag = df_tag.stack().reset_index()
            df_tag = df_tag.drop("level_0", axis=1)
            df_tag = df_tag.drop("level_1", axis=1)

            #reformat cols to entity_sets layout and eliminate node duplicates
            df_tag[1] = ''
            df_tag[2] = ''
            df_tag[3] = ''
            #create column 4 with node number and suffix ','
            df_tag[4] = df_tag[0].astype(int).astype(str) + ','
            #eliminate duplicate node indices on tagged surface, empty column 0
            df_tag = df_tag.drop_duplicates(subset=[0])
            df_tag[0] = ''
            # remove suffix ',' from last row of nodes, reset indices
            df_tag.loc[df_tag.index[-1], 4] = df_tag.loc[df_tag.index[-1],
                                                         4].rstrip(",")
            df_tag = df_tag.reset_index().drop("index", axis=1)

            # - 5.3 Create header dataframes -
            #create headers
            # yapf: disable
            df_entity_sets_start = pd.DataFrame([
                ['{', '', '', '', '',],
                ['', '"node_sets": [', '', '', '',],
                ['', '', '{', '', '',],
                ['', '', '', '"id": '+str(tag)+',', '',],
                ['', '', '', '"set": [', '',]]) #start header
            df_entity_sets_join = pd.DataFrame([
                ['', '', '', ']', '',],
                ['', '', '},', '', '',],
                ['', '', '{', '', '',],
                ['', '', '', '"id": '+str(tag)+',', '',],
                ['', '', '', '"set": [', '',]]) #middle header
            # yapf: enable

            #select whether first entity set header or not
            if tag == first_tag:
                df_entity_sets_pre = df_entity_sets_start  #start header
            else:
                df_entity_sets_pre = df_entity_sets_join  #middle header

            # - 5.4 Concatenate each surface dataframe & format (inside loop) -
            df_entity_sets = pd.concat(
                [df_entity_sets, df_entity_sets_pre, df_tag],
                axis=0,
                ignore_index=True)

        # - 5.5 Add footer to dataframe (outside loop) -
        df_entity_sets = pd.concat([df_entity_sets, df_entity_sets_end],
                                   axis=0,
                                   ignore_index=True)

        # - 5.6 Export to tagged entity_sets_file as a .json -
        if not os.path.isfile(in_dir1 + entity_sets_file + '.json'):
            df_entity_sets.to_csv(in_dir1 + entity_sets_file + '.json',
                                  index=False,
                                  header=False,
                                  sep='\t',
                                  quoting=3)
        else:
            if dflag == True:
                os.remove(in_dir1 + entity_sets_file + '.json')
                df_entity_sets.to_csv(in_dir1 + entity_sets_file + '.json',
                                      index=False,
                                      header=False,
                                      sep='\t',
                                      quoting=3)
                print("Entity sets file " + str(entity_sets_file) +
                      ".json overwritten")
            else:
                print("Entity sets file " + str(entity_sets_file) +
                      ".json already exists... quitting")
                quit()

    # --- 6.0 VELOCITY_CONSTRAINTS.TXT ---
    if velocity_constraints_flag == True:

        # - 6.1 Create & format parts, then concatenate to dataframe -
        df_velocity_constraints = pd.DataFrame()
        #loop through surfaces, ignore surfaces with no BCs
        for tag, tuple_loop in Surface_tags.items():
            if not (len(tuple_loop) == 0 or all(x is None
                                                for x in tuple_loop)):
                # - 6.2 Get desired node indices on each surface of interest -
                df_tag = df_e
                #slice to get only elements on tagged surface
                df_tag = df_tag.loc[(df_tag[3] == tag), [5, 6, 7, 8]]
                #create 1 col of all node indices for elements on tagged surface
                df_tag = df_tag.stack().reset_index()
                df_tag = df_tag.drop("level_0", axis=1)
                df_tag = df_tag.drop("level_1", axis=1)
                #remove duplicate node indices on tagged surface, reset indices
                df_tag = df_tag.drop_duplicates(subset=[0])
                df_tag = df_tag.reset_index().drop("index", axis=1)

                # - 6.3 Create node indices, BCs for each direction needed -
                #create/reset empty dataframe for each surface
                df_tag_temp1 = pd.DataFrame()
                df_tag_temp2 = pd.DataFrame()
                #loop through directions, ignore directions with no BCs
                for i in range(len(tuple_loop)):
                    if not tuple_loop[i] == None:
                        #rows: 0 = node indices, 1 = direction, 2 = BC magnitude
                        df_tag_temp1[0] = df_tag[0].astype(int)
                        df_tag_temp1[1] = i
                        df_tag_temp1[2] = tuple_loop[i]
                        #concatenate direction i to surface-specific dataframe
                        df_tag_temp2 = pd.concat([df_tag_temp2, df_tag_temp1],
                                                 axis=0,
                                                 ignore_index=True)

                df_tag = df_tag_temp2
                #reset indices, reset headers
                df_tag = df_tag.reset_index().drop("index", axis=1)
                df_tag.columns = range(df_tag.columns.size)

                #assemble velocity_constraints.txt df by concatenating surfaces
                df_velocity_constraints = pd.concat(
                    [df_velocity_constraints, df_tag],
                    axis=0,
                    ignore_index=True)

        # - 6.4 Export to .txt velocity_constraints_file -
        if not os.path.isfile(in_dir1 + velocity_constraints_file):
            df_velocity_constraints.to_csv(in_dir1 + velocity_constraints_file,
                                           index=False,
                                           header=False,
                                           sep=' ')
        else:
            if dflag == True:
                os.remove(in_dir1 + velocity_constraints_file)
                df_velocity_constraints.to_csv(in_dir1 +
                                               velocity_constraints_file,
                                               index=False,
                                               header=False,
                                               sep=' ')
                print("Velocity constraints file '%s' overwritten" %
                      velocity_constraints_file)
            else:
                print(
                    "Velocity constraints file '%s' already exists... quitting"
                    % velocity_constraints_file)
                quit()


# --------------------------------------------------------------------
# --- MAIN ---
gmsh_converter_tet(in_dir, ori_file, mesh_flag, entity_sets_flag,
                   velocity_constraints_flag, Surface_Zmin, Surface_Ymin,
                   Surface_Xmax, Surface_Ymax, Surface_Xmin, Surface_Zmax)
