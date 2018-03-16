from tkinter import *
from tkinter.ttk import *
''' Define and display IDEF0 diagrams of occurrences, being activities or processes.
    The diagrams have a hierarchy,
    whereby the parts of an occurrence are presented on a next page
'''
class Occurrences_diagram():
    def __init__(self, user_interface, gel_net):
        self.root = user_interface.root
        self.gel_net = gel_net
        self.GUI_lang_index = user_interface.GUI_lang_index
        self.seq_table = user_interface.views.seq_table
        self.involv_table = user_interface.views.involv_table
        #self.parts_of_occ_table = user_interface.views.parts_of_occ_table
        self.part_whole_occs = user_interface.views.part_whole_occs
        
        self.drawings = []
        self.sheets = []
        self.leftStrFrame = []
        self.rightStrFrame = []
        self.leftStrTree = []
        self.rightStrTree = []
        self.leftStrScroll = []
        self.rightStrScroll = []
        self.draw_x_scroll = []
        self.draw_y_scroll = []
        self.boxes = []
        self.lines = []
        self.part = []
        
    def Define_Notebook_for_drawings(self):
        """ Define a Notebook for drawings and call partRelList function."""

        #w = 1000                # pixels of canvas
        #h = 600                 # pixels of canvas

    # Occurrences drawings Windows root
        heading = ['Activities according to IDEF0','Activiteiten volgens IDEF0']
        occWindow = Toplevel(self.root) # ,width=w,height=h
        occWindow.title(heading[self.GUI_lang_index])
        self.screen_width = occWindow.winfo_screenwidth() - 36
        self.screen_height = occWindow.winfo_screenheight() - 200
        occWindow.configure(width=self.screen_width, height=self.screen_height)
        occWindow.minsize(width=800, height=400)
        occWindow.columnconfigure(0, weight=1)
        #occWindow.columnconfigure(1, weight=1)
        occWindow.rowconfigure(0, weight=1)
        #occWindow.rowconfigure(1, weight=0)

        occFrame = ttk.Frame(occWindow)  # columnspan
        occFrame.columnconfigure(0, weight=1)
        occFrame.rowconfigure(0, weight=1)
        #occFrame.rowconfigure(1, weight=1)
        occFrame.grid(column=0,row=0, sticky=NSEW) # columnspan=2,
        
        self.occ_notebook = ttk.Notebook(occFrame) #, height=600, width=1200)
        self.occ_notebook.columnconfigure(0, weight=1)
        self.occ_notebook.rowconfigure(0, weight=1)
        #self.occ_notebook.rowconfigure(1, weight=1)
        self.occ_notebook.grid(column=0, row=0, sticky=NSEW)

    #-----------------------------------------------------------
    def Create_occurrences_diagram(self, top_occs):
        """ Prepare for the drawing of one or more IDEF0 sheets
            about one hierarchy of occurrences
            in the product model.
            nrOfOccs: length of chain of sequence occurrences.
            occ_table: same columns as exprTable with all relations
                       that deal with occurrences in the product model.
            seq_table: previusUID, previusName, nextUID, nextName
            involv_table: occurUID, occurName, involvedUID, involvedName,
                          roleUID, roleName of involved object.
            part_whole_occs: whole, part, kind_of_part
        """
        test = False

        self.sheet_nr = -1

##    # Determine top(s) of composition hierarchy/hierarchies
##        # Determine occurrences on topsheet
##        top_occs  = []
##        topNames = []
##        partRelList = [row[i] for row in self.part_whole_occs for i in range(2,3)]
##        for row2 in self.part_whole_occs:
##            # If uid of whole not in the list of part_uids, then append
##            if  row2[0] != partRelList and row2[1] not in topNames:
##                top_occs.append(row2[0])
##                topNames.append(row2[1])  # wholeName is a name of a top occurrence

        if len(top_occs) == 0:
            if test: print('*** No top occurrence identified')
            return
        else:
            if test: print('*** Number top occurrence {}:'.format(len(top_occs)))

    # Initialize drawing
        self.Define_Notebook_for_drawings()
    # Draw top occurrences on one or more sheet(s)
        parentID = 0
        self.MultipleSheets(parentID, top_occs)

    # Determine parts per top occurrence for drawing on sheet(s)
        self.DrawPartOccurrences(parentID, top_occs)

    #--------------------------------------------------------
    def MultipleSheets(self, parentID, occs):
        """ Determine nr of sheets for one drawing and call DrawingOfOneSheet
            totalNrOfBoxes to be drawn on one drawing
            may require more than one drawing sheet.
        """
        totalNrOfBoxes = len(occs)
        maxBoxesPerSheet = 7
        firstBox = 0
        
        nrOfSheets = (totalNrOfBoxes-1)/maxBoxesPerSheet + 1
        intSheet = int(nrOfSheets)
        rest = totalNrOfBoxes - (intSheet-1)*maxBoxesPerSheet
        shText  = str(parentID)
        #print('nrOfSheets on level, totalNrOfBoxes, rest:',
        #      intSheet, totalNrOfBoxes, occs[0].name, rest, shText)
        for shNr in range(1,intSheet+1):
            if shNr == intSheet:
                nrBoxesPerSheet = rest
            else:
                nrBoxesPerSheet = maxBoxesPerSheet
            self.sheet_nr += + 1
            schema = ['Sheet-' + shText, 'Blad-' + shText]
            sheetName = schema[self.GUI_lang_index]
            # Initialize drawing for one sheet.
            self.Define_DrawingOfOneSheet(sheetName)
            # Draw one sheet
            self.Draw_DrawingOfOneSheet(nrBoxesPerSheet, occs[firstBox:], parentID)
            firstBox = firstBox + maxBoxesPerSheet
            shText = shText + '-' + str(shNr)

#--------------------------------------------------------
    def DrawPartOccurrences(self, parentID, occs):
        ''' Draw the diagram(s) of the parts of the occurrences occs
            self.part_whole_occs: whole, part, kind_of_part
        '''
        parts = []
        #partNames= []
        parts_present = False
        seq = 0
        for topOcc in occs:
            seq = seq + 1
            childID = str(parentID) + '.' + str(seq)
            for whole, part, kind_of_part in self.part_whole_occs:
                # If the whole appears on previous sheet, then there is a part:
                if  whole == topOcc:
                    parts_present = True
                    #nrOfOccs = nrOfOccs + 1     # nr of occurrences on sheet
                    parts.append(part)
                    #partNames.append(part.name) # wholeName is a name of a top occurrence
    # Draw part occurrences on sheet(s)
            if parts_present is True:
                self.MultipleSheets(childID, parts)
            
        if parts_present is True:
            self.DrawPartOccurrences(childID, parts)
        return
#--------------------------------------------------------

    def RightMouseButton(self, event):
        ''' Handle right mouse button click events in occurModel (actTree):
            Determine mid_point coordinates in box_type_1
        '''

        # x,y = Nr of pixels
        print('Activity details: x = %d, y = %d' % (event.x, event.y))
        name = ''
        midPts = self.BoxType1(self.sheets[self.sheet_nr], event.x, event.y, name)
        
        return midPts
    #-------------------------------------------------------------
    def Define_DrawingOfOneSheet(self, sheetName):
        """ Create a Notebook page and draw one sheet on that page by calling BoxType1
            and draw lines between them by calling CreateLine.
        """
    # Occurrences drawing Frame tab
        self.drawings.append(ttk.Frame(self.occ_notebook))
        self.drawings[self.sheet_nr].grid(column=0,row=0,sticky=NSEW)
        self.drawings[self.sheet_nr].columnconfigure(0,weight=1)
        self.drawings[self.sheet_nr].columnconfigure(1,weight=1)
        self.drawings[self.sheet_nr].rowconfigure(0,weight=1)
        self.drawings[self.sheet_nr].config(borderwidth=5)
        #self.drawings[self.sheet_nr].rowconfigure(1,weight=1)
        self.occ_notebook.add(self.drawings[self.sheet_nr], text=sheetName, sticky=NSEW)
        self.occ_notebook.insert("end",self.drawings[self.sheet_nr],sticky=NSEW)

        #self.sheets = Canvas(drawing, width=self.screen_width, \
        #                     height=self.screen_height, background='#ddf')
        self.sheets.append(Canvas(self.drawings[self.sheet_nr], width=self.screen_width-100,\
                                  height=self.screen_height-200, background='#ddf')) # Canvas
        self.sheets[self.sheet_nr].grid(column=0,row=0,columnspan=2,sticky=NSEW)
        self.sheets[self.sheet_nr].bind('<Button-2>', self.RightMouseButton)
        self.sheets[self.sheet_nr].columnconfigure(0,weight=1)
        self.sheets[self.sheet_nr].rowconfigure(0,weight=1)
        #self.sheets[self.sheet_nr].rowconfigure(1,weight=1)

        self.draw_y_scroll.append(ttk.Scrollbar(self.drawings[self.sheet_nr],\
                                                orient=VERTICAL,\
                                                command=self.sheets[self.sheet_nr].yview))
        self.draw_y_scroll[self.sheet_nr].grid (column=2,row=0,sticky=NS+E)
        self.sheets[self.sheet_nr].config(yscrollcommand=self.draw_y_scroll[self.sheet_nr].set)
        self.draw_x_scroll.append(ttk.Scrollbar(self.drawings[self.sheet_nr],\
                                                orient=HORIZONTAL,\
                                                command=self.sheets[self.sheet_nr].xview))
        self.draw_x_scroll[self.sheet_nr].grid (column=0,row=1,columnspan=2,sticky=S+EW)
        self.sheets[self.sheet_nr].config(xscrollcommand=self.draw_x_scroll[self.sheet_nr].set)

    # Stream Frames - left and right
        self.leftStrFrame.append(ttk.Frame(self.drawings[self.sheet_nr]))
        self.leftStrFrame[self.sheet_nr].columnconfigure(0, weight=1)
        self.leftStrFrame[self.sheet_nr].rowconfigure(0, weight=0)
        self.leftStrFrame[self.sheet_nr].rowconfigure(1, weight=1)
        self.leftStrFrame[self.sheet_nr].grid(column=0, row=2, sticky=NSEW)

        self.rightStrFrame.append(ttk.Frame(self.drawings[self.sheet_nr]))
        self.rightStrFrame[self.sheet_nr].columnconfigure(0, weight=1)
        self.rightStrFrame[self.sheet_nr].rowconfigure(0, weight=0)
        self.rightStrFrame[self.sheet_nr].rowconfigure(1, weight=1)
        self.rightStrFrame[self.sheet_nr].grid(column=1, row=2, sticky=NSEW)

        self.leftStrTree.append(ttk.Treeview(
            self.leftStrFrame[self.sheet_nr], \
            columns=('strNr','strName','strUID','strKind'),\
            displaycolumns =('strNr','strName','strUID','strKind'),\
            selectmode='browse',height=5))

        self.rightStrTree.append(ttk.Treeview(
            self.rightStrFrame[self.sheet_nr],\
            columns=('strNr','strName','strUID','strKind'),\
            displaycolumns=('strNr','strName','strUID','strKind'),
            selectmode='browse',height=5))

        sNrText = ['Number','Nummer']
        strText = ['Stream Name','Stroomnaam']
        uidText = ['UID'   ,'UID']
        kinText = ['Kind'  ,'Soort']
        self.leftStrTree[self.sheet_nr].heading('strNr'   ,text=sNrText[self.GUI_lang_index] ,anchor=W)
        self.leftStrTree[self.sheet_nr].heading('strName' ,text=strText[self.GUI_lang_index] ,anchor=W)
        self.leftStrTree[self.sheet_nr].heading('strUID'  ,text=uidText[self.GUI_lang_index] ,anchor=W)
        self.leftStrTree[self.sheet_nr].heading('strKind' ,text=kinText[self.GUI_lang_index] ,anchor=W)
        self.rightStrTree[self.sheet_nr].heading('strNr'   ,text=sNrText[self.GUI_lang_index] ,anchor=W)
        self.rightStrTree[self.sheet_nr].heading('strName' ,text=strText[self.GUI_lang_index] ,anchor=W)
        self.rightStrTree[self.sheet_nr].heading('strUID'  ,text=uidText[self.GUI_lang_index] ,anchor=W)
        self.rightStrTree[self.sheet_nr].heading('strKind' ,text=kinText[self.GUI_lang_index] ,anchor=W)
        
        self.leftStrTree[self.sheet_nr].column('#0'       ,minwidth=10,width=10)
        self.leftStrTree[self.sheet_nr].column('strNr'    ,minwidth=20,width=40)
        self.leftStrTree[self.sheet_nr].column('strName'  ,minwidth=20,width=120)
        self.leftStrTree[self.sheet_nr].column('strUID'   ,minwidth=20,width=60)
        self.leftStrTree[self.sheet_nr].column('strKind'  ,minwidth=20,width=100)
        self.rightStrTree[self.sheet_nr].column('#0'       ,minwidth=10,width=10)
        self.rightStrTree[self.sheet_nr].column('strNr'    ,minwidth=20,width=40)
        self.rightStrTree[self.sheet_nr].column('strName'  ,minwidth=20,width=120)
        self.rightStrTree[self.sheet_nr].column('strUID'   ,minwidth=20,width=60)
        self.rightStrTree[self.sheet_nr].column('strKind'  ,minwidth=20,width=100)

        self.leftStrTree[self.sheet_nr].grid(column=0,row=0,sticky=NSEW)
        self.rightStrTree[self.sheet_nr].grid(column=0,row=0,sticky=NSEW)

        self.leftStrTree[self.sheet_nr].columnconfigure(0,weight=1)
        self.leftStrTree[self.sheet_nr].columnconfigure(1,weight=1)
        self.leftStrTree[self.sheet_nr].rowconfigure(0,weight=0)
        self.leftStrTree[self.sheet_nr].rowconfigure(1,weight=1)
        self.rightStrTree[self.sheet_nr].columnconfigure(0,weight=1)
        self.rightStrTree[self.sheet_nr].columnconfigure(1,weight=1)
        self.rightStrTree[self.sheet_nr].rowconfigure(0,weight=0)
        self.rightStrTree[self.sheet_nr].rowconfigure(1,weight=1)

        self.leftStrTree[self.sheet_nr].tag_configure('uomTag', option=None, background='#ccf')
        self.leftStrTree[self.sheet_nr].tag_configure('occTag', option=None, background='#cfc')
        self.rightStrTree[self.sheet_nr].tag_configure('uomTag', option=None, background='#ccf')
        self.rightStrTree[self.sheet_nr].tag_configure('occTag', option=None, background='#cfc')

        self.leftStrScroll.append(ttk.Scrollbar(self.leftStrFrame[self.sheet_nr],orient=VERTICAL,command=self.leftStrTree[self.sheet_nr].yview))
        self.leftStrScroll[self.sheet_nr].grid (column=0,row=0,sticky=NS+E)
        self.leftStrTree  [self.sheet_nr].config(yscrollcommand=self.leftStrScroll[self.sheet_nr].set)
        
        self.rightStrScroll.append(ttk.Scrollbar(self.drawings[self.sheet_nr],orient=VERTICAL,command=self.rightStrTree[self.sheet_nr].yview))
        self.rightStrScroll[self.sheet_nr].grid (column=2,row=2,sticky=NS+E)
        self.rightStrTree  [self.sheet_nr].config(yscrollcommand=self.rightStrScroll[self.sheet_nr].set)

    def Draw_DrawingOfOneSheet(self, nrOfOccs, occs, parentID):
        ''' - parentID: the ID of the whole occurrence (box) of which the occNames (occurrences) are parts.
        '''
        test = False
        
        outputUID = '640019'      # output role
        inputUID  = '640016'      # input role
        actorUID  = '5036'        # actor role (supertype of mechanism)
        subOutputs, subOutputUIDs = self.gel_net.Determine_subtype_list(outputUID)
        subInputs,  subInputUIDs  = self.gel_net.Determine_subtype_list(inputUID)
        subActors,  subActorUIDs  = self.gel_net.Determine_subtype_list(actorUID)

        thick = 2
        centerX  = []            # X-Center of canvas
        centerY  = []            # Y-Center of canvas
        midPts   = []
        boxesOnSheet = []
        linesOnSheet = []

        boxWidth  = 100          # pixels
        boxHeight = 100          # pixels
        self.boxW2 = boxWidth  / 2   # 1/2Width  of boxes
        self.boxH2 = boxHeight / 2   # 1/2Height of boxes

        deltaX = self.screen_width/(nrOfOccs+1)
        deltaY = self.screen_height/(nrOfOccs+1)
        dxC = 8                 # corner rounding
        dyC = 8
        dx  = 8                 # shifted start point for line on box
        dy  = 8

        occIn  = []
        occOut = []
        occCon = []
        occMech= []
        occInUp  = []
        occOutUp = []
        occConUp = []
        occMechUp= []
    # Draw boxes (occurrences), return midpts[i] = N(x,y),S(x,y),E(x,y),W(x,y)
        for boxNr in range(0,nrOfOccs):
            centerX.append(deltaX + boxNr*deltaX)     # X of center of box canvas
            centerY.append(deltaY + boxNr*deltaY)     # Y of center of box canvas
            self.boxID = str(parentID) + '.' + str(boxNr+1)

            midPts.append(self.BoxType1(self.sheets[self.sheet_nr], \
                                        centerX[boxNr], centerY[boxNr], \
                                        occs[boxNr].name))

            if test: print('NSEWPts:',boxNr,midPts[boxNr])
        self.boxes.append(boxesOnSheet)
        
    # initialize number of I/O/C/M down and upwards for each occurrence on sheet
        occIn     = [0 for i in range(0,nrOfOccs)]  # input stream nr of deltas downward
        occOut    = [0 for i in range(0,nrOfOccs)]
        occCon    = [0 for i in range(0,nrOfOccs)]  # control stream nr of deltas right
        occMech   = [0 for i in range(0,nrOfOccs)]
        occInUp   = [0 for i in range(0,nrOfOccs)]  # input stream nr of deltas upward
        occOutUp  = [0 for i in range(0,nrOfOccs)]
        occConUp  = [0 for i in range(0,nrOfOccs)]  # control stream nr of deltas left
        occMechUp = [0 for i in range(0,nrOfOccs)]
            
    # Draw lines (streams)
        strNr = 0
        rsize = 20          # size of the rhombus polygon
        left  = True        # indicator for left or right streamTree.
        border = 5
        
    # Search for lines that have no begin/source occurrence (box), but only a destination occurrence.      
        for occur, involved, inv_role_kind, inv_kind_name in self.involv_table:
            #print('ioRow[0]:', occur.uid, occur.name, involved.name, inv_role_kind.name)
            occUIDFrom = '0'
            # If inputStream to occurrence on this sheet, then
            if occur in occs and inv_role_kind.uid in subInputUIDs:
                # IndexTo is the nr of the occ that has stream as input.
                indexTo = occs.index(occur)

                # Verify whether found stream is an output of any box on sheet, then set out = True
                out = False
                for occur_2, involved_2, inv_role_kind_2, inv_kind_name_2 in self.involv_table: #row2
                    if involved == involved_2 and occur_2 in occs and inv_role_kind_2.uid in subOutputUIDs:
                        out = True
                        break
                    
                if out is False:
                    # Input comes from outside the sheet
                    streamUID  = involved.uid
                    streamName = involved.name
                    streamKind = inv_kind_name
                    occIn  [indexTo] += 1
                    occInUp[indexTo] += 1
                    strNr = strNr + 1
                    strID = str(strNr)
                    endPt = midPts[indexTo][3]
                    beginPt = [border,midPts[indexTo][3][1]]
                    
                    x = (beginPt[0] + endPt[0])/2
                    y =  beginPt[1]
                    rhombus = self.RhombusPolygon(self.sheets[self.sheet_nr], x, y, strID, rsize)
                    
                    lConnPt = rhombus[3]
                    rConnPt = rhombus[2]
                    line1Pts = [beginPt,lConnPt]
                    line2Pts = [rConnPt,endPt]
                    
                    line1 = self.sheets[self.sheet_nr].create_line(line1Pts,fill='blue', width=thick, arrow=LAST)
                    line2 = self.sheets[self.sheet_nr].create_line(line2Pts,fill='blue', width=thick, arrow=LAST)
                    linesOnSheet.append(line1)
                    if left is True:
                        self.leftStrTree[self.sheet_nr].insert('',index='end',values=(strID,streamName,streamUID,streamKind),tags='occTag')
                        left = False
                    else:
                        self.rightStrTree[self.sheet_nr].insert('',index='end',values=(strID,streamName,streamUID,streamKind),tags='occTag')
                        left = True
    # Find streams per occurrence (box) on this sheet in involv_table
    #  involv_table:   occurUID,   occurName, involvedUID, involvedName, roleUID, roleName of involved object.
        if test: print ('subI/O-UIDs:',occs[0].name, subInputUIDs, subOutputUIDs)
        for occ, involved, inv_role_kind, inv_kind_name in self.involv_table:
            if test: print(' ioRow2:',occs[0].name, occ.name, involved.name, inv_role_kind.uid)
            occUIDTo = '0'
            # If outputStream from occurrence on this sheet, then
            if occ in occs and inv_role_kind.uid in subOutputUIDs:
                if test: print('**outputStream:',involved.name, inv_role_kind.name)
                strNr = strNr + 1
                strID = str(strNr)
                occUIDFrom = occ.uid
                streamUID  = involved.uid
                streamName = involved.name
                streamKind = inv_kind_name
                # Verify if found streamUID is input in box on sheet. If yes, then occUIDTo is known
                for occ_2, involved_2, inv_role_kind_2, inv_kind_name_2 in self.involv_table:
                    if streamUID == involved_2.uid and occ_2 in occs and inv_role_kind_2.uid in subInputUIDs: 
                        if test: print('** inputStream:',occ_2.name, inv_role_kind_2.name, inv_role_kind_2.name)
                        occUIDTo = occ_2.uid
                        # else occUIDTo remains '0'
                        break
                # Determine index (in list of occs) of boxFrom and boxTo 
                indexFrom = -1
                indexTo   = -1
                for index in range(0,len(occs)):
                    if occUIDFrom == occs[index].uid:
                        indexFrom = index
                    if occUIDTo == occs[index].uid:
                        indexTo = index

                # Determine the sequenceNr of the input and output of the occurrence box
                # and adjust Yin and Yout accordingly.            
                # Draw the stream line from box occUIDFrom to occUIDTo or to edge of sheet.
                if indexTo == -1:
                    # No destination box, thus endPt is on rh side of the sheet.
                    ddyFrom   = (occOut  [indexFrom])*dy
                    ddyTo     = (occIn   [indexTo])*dy
                    if occOut[indexFrom] == 0:
                        # if not yet started downward, then middle becomes occupied.
                        occOutUp[indexFrom] += 1
                    occOut  [indexFrom] += 1
                    #occOut[indexTo]   += 1         # indexTo == -1
                    # midPts(occNr,East,x/y)
                    beginPt = [midPts[indexFrom][2][0],midPts[indexFrom][2][1] + ddyFrom]
                    endPt = [self.screen_width-border,beginPt[1]]
                    x = (beginPt[0] + endPt[0])/2
                    y =  beginPt[1]
                    # Rhombus on vertical line
                    rhombus = self.RhombusPolygon(self.sheets[self.sheet_nr],x,y,strID,rsize)
                    lConnPt = rhombus[3]
                    rConnPt = rhombus[2]
                    line1Pts = [beginPt,lConnPt]
                    line2Pts = [rConnPt,endPt]
                    
                elif indexFrom + 1 < indexTo:       # destination box is behind next box.
                    ddyFrom   = (occOut  [indexFrom])*dy
                    ddyTo     = (occIn   [indexTo])*dy
                    occOut[indexFrom] += 1
                    occOut[indexTo]   += 1
                    beginPt = [midPts[indexFrom][2][0],midPts[indexFrom][2][1] + ddyFrom]
                    endPt   = [midPts[indexTo][3][0],  midPts[indexTo][3][1]   + ddyTo]
                    mid1Pt  = [(beginPt[0] + midPts[indexFrom+1][3][0])/2 - dxC, beginPt[1]]
                    mid2Pt  = [(beginPt[0] + midPts[indexFrom+1][3][0])/2      , beginPt[1] + dyC]
                    mid3Pt  = [(beginPt[0] + midPts[indexFrom+1][3][0])/2      , endPt[1] - dyC]
                    mid4Pt  = [(beginPt[0] + midPts[indexFrom+1][3][0])/2 + dxC, endPt[1]]
                    x =  mid2Pt[0]
                    y = (mid2Pt[1] + mid3Pt[1])/2
                    rhombus = self.RhombusPolygon(self.sheets[self.sheet_nr],x,y,strID,rsize)
                    uConnPt = rhombus[0]
                    lConnPt = rhombus[1]
                    line1Pts = [beginPt, mid1Pt, mid2Pt, uConnPt]
                    line2Pts = [lConnPt, mid3Pt, mid4Pt, endPt]
                    
                elif indexFrom + 1 > indexTo:       # destination box id before source box (or the box itself).
                    ddyUpFrom = (occOutUp[indexFrom])*dy
                    ddyUpTo   = (occInUp [indexTo])*dy
                    occOutUp[indexFrom] += 1
                    occOutUp[indexTo]   += 1
                    beginPt = [midPts[indexFrom][2][0],midPts[indexFrom][2][1] - ddyUpFrom]
                    endPt   = [midPts[indexTo][3][0],   midPts[indexTo][3][1]  - ddyUpTo]
                    mid1Pt  = [(beginPt[0] + midPts[indexFrom+1][3][0])/2 - dxC, beginPt[1]]
                    mid2Pt  = [(beginPt[0] + midPts[indexFrom+1][3][0])/2      , beginPt[1] - dyC]
                    mid3Pt  = [(beginPt[0] + midPts[indexFrom+1][3][0])/2      , endPt[1] - boxHeight + dyC]
                    mid4Pt  = [(beginPt[0] + midPts[indexFrom+1][3][0])/2 - dxC, endPt[1] - boxHeight]
                    mid5Pt  = [(endPt[0] - boxWidth/2) + dxC, endPt[1] - boxHeight]
                    mid6Pt  = [(endPt[0] - boxWidth/2)      , endPt[1] - boxHeight + dyC]
                    mid7Pt  = [(endPt[0] - boxWidth/2)      , endPt[1]             - dyC]
                    mid8Pt  = [(endPt[0] - boxWidth/2) + dxC, endPt[1]                  ]
                    x =  mid2Pt[0]
                    y = (mid2Pt[1] + mid3Pt[1])/2
                    rhombus = self.RhombusPolygon(self.sheets[self.sheet_nr],x,y,strID,rsize)
                    uConnPt = rhombus[0]
                    lConnPt = rhombus[1]
                    line1Pts = [beginPt, mid1Pt, mid2Pt, lConnPt]
                    line2Pts = [uConnPt, mid3Pt, mid4Pt, mid5Pt,\
                                mid6Pt,  mid7Pt, mid8Pt, endPt]
                                
                    if mid5Pt[1] < 0:
                        self.sheets[self.sheet_nr].yview_scroll(int(-mid5Pt[1]) + 20, 'units')
                else:                               # destination box is nex box
                    ddyFrom   = (occOut  [indexFrom])*dy
                    ddyUpTo   = (occIn   [indexTo])*dy
                    occOut[indexFrom] += 1
                    occOutUp[indexTo] += 1
                    beginPt = [midPts[indexFrom][2][0],midPts[indexFrom][2][1] + ddyFrom]                  
                    endPt   = [midPts[indexTo][3][0],  midPts[indexTo][3][1]   - ddyUpTo]
                    mid1Pt  = [(beginPt[0] + endPt[0])/2 - dxC, beginPt[1]]
                    mid2Pt  = [(beginPt[0] + endPt[0])/2      , beginPt[1] + dyC]
                    mid3Pt  = [(beginPt[0] + endPt[0])/2      , endPt[1]   - dyC]
                    mid4Pt  = [(beginPt[0] + endPt[0])/2 + dxC, endPt[1]]
                    x =  mid2Pt[0]
                    y = (mid2Pt[1] + mid3Pt[1])/2
                    rhombus = self.RhombusPolygon(self.sheets[self.sheet_nr],x,y,strID,rsize)
                    uConnPt = rhombus[0]
                    lConnPt = rhombus[1]
                    line1Pts = [beginPt, mid1Pt, mid2Pt, uConnPt]
                    line2Pts = [lConnPt, mid3Pt, mid4Pt, endPt]
                if test: print('  Stream:',indexFrom,indexTo,line1Pts)
                line1 = self.sheets[self.sheet_nr].create_line(line1Pts,fill='blue', width=thick, arrow=LAST)
                line2 = self.sheets[self.sheet_nr].create_line(line2Pts,fill='blue', width=thick, arrow=LAST)
                linesOnSheet.append(line1)
    # Record stream in leftStrTree[self.sheet_nr](s)
                if left is True:
                    self.leftStrTree[self.sheet_nr].insert('',index='end',values=(strID,streamName,streamUID,streamKind),tags='occTag')
                    left = False
                else:
                    self.rightStrTree[self.sheet_nr].insert('',index='end',values=(strID,streamName,streamUID,streamKind),tags='occTag')
                    left = True
                
        self.lines.append(linesOnSheet)
        return
    #-----------------------------------------------------------
    def BoxType1(self, sheet, X, Y, name):
        """Draw a box around (X,Y) = Xcenter and Ycenter
        Return midpts = N(x,y),S(x,y),E(x,y),W(x,y)
        (X,Y) = center of box on canvas"""

        x0,y0 = X - self.boxW2, Y - self.boxH2        # TopLeft of box
        x1,y1 = X + self.boxW2, Y + self.boxH2        # BottomRight of box

        boxNr = sheet.create_rectangle(x0, y0, x1, y1, \
                               fill='#dfd', outline='black')
        boxName  = sheet.create_text(X,Y,justify=CENTER,text=name)
        boxIdent = sheet.create_text(X,Y+15,justify=CENTER,text=str(self.boxID))

        midNorth = [X        , Y - self.boxH2]
        midSouth = [X        , Y + self.boxH2]
        midEast  = [X + self.boxW2, Y]
        midWest  = [X - self.boxW2, Y]

        return midNorth,midSouth,midEast,midWest
    #-----------------------------------------------------------
    def RhombusPolygon(self, sheet, X, Y, strID, rsize):
        """Draw a rhombus polygon on position X,Y with its strID as text in the middle on sheet."""

        x0,y0 = X - rsize, Y             # midWest
        x1,y1 = X        , Y - rsize     # midNorth
        x2,y2 = X + rsize, Y             # midEast
        x3,y3 = X        , Y + rsize     # midSouth
        rhomNr = sheet.create_polygon(x0,y0,x1,y1,x2,y2,x3,y3,\
                             fill='#dfd', smooth=0, outline='black')
        strIdent = sheet.create_text(X,Y,justify=CENTER,text=strID)

        midNorth = [x1,y1]
        midSouth = [x3,y3]
        midEast  = [x2,y2]
        midWest  = [x0,y0]
        
        return midNorth,midSouth,midEast,midWest
    #-----------------------------------------------------------
    def exit_python(self, event):
        '''Exit Python when the event 'event' occurs.'''
        quit() # no arguments to quit 
