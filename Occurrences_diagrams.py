class Occurrences_diagram():
    def __init__(self):
        self.drawings = []
        self.sheet    = []
        self.leftStrFrame  = []
        self.rightStrFrame = []
        self.leftStrTree   = []
        self.rightStrTree  = []
        self.leftStrScroll  = []
        self.rightStrScroll = []
        self.drawXScroll = []
        self.drawYScroll = []
        self.boxes    = []
        self.lines    = []
        self.part     = []
        
    def Create_occurrences_diagram():
        """ Define a Notebook for drawings and call partRelList function."""
        
        global scrWidth,scrHeight, occNoteb

        #from tkinter import *
        #from tkinter import ttk

        #w = 1000                # pixels of canvas
        #h = 600                 # pixels of canvas

    # Occurrences drawings Windows root
        heading = ['Activities according to IDEF0','Activiteiten volgens IDEF0']
        occWindow = Toplevel(root) # ,width=w,height=h
        occWindow.title(heading[langGUIIndex])
        scrWidth  = occWindow.winfo_screenwidth() - 36
        scrHeight = occWindow.winfo_screenheight() - 200
        occWindow.configure(width=scrWidth,height=scrHeight)
        occWindow.minsize(width=800,height=400)
        occWindow.columnconfigure(0,weight=1)
        #occWindow.columnconfigure(1,weight=1)
        occWindow.rowconfigure(0,weight=1)
        #occWindow.rowconfigure(1,weight=0)

        occFrame = ttk.Frame(occWindow)  # columnspan
        occFrame.columnconfigure(0,weight=1)
        occFrame.rowconfigure(0,weight=1)
        #occFrame.rowconfigure(1,weight=1)
        occFrame.grid(column=0,row=0,sticky=NSEW) #pack(fill='both',side=TOP) # columnspan=2,
        
        occNoteb  = ttk.Notebook(occFrame) #, height=600, width=1200)
        occNoteb.columnconfigure(0,weight=1)
        occNoteb.rowconfigure(0,weight=1)
        #occNoteb.rowconfigure(1,weight=1)
        occNoteb.grid(column=0,row=0,sticky=NSEW) #pack(fill='both') #  #
        
        Drawings()

    #-----------------------------------------------------------
    def Drawings():
        """Prepare for the drawing of one or more IDEF0 sheets about one hierarchy of occurrences
    in the product model.
    nrOfOccs: length of chain of sequence occurrences.
    occTable:  same columns as exprTable with all relations that deal with occurrences in the product model.
    seqTable:  previusUID, previusName, nextUID,     nextName
    ioTable:   occurUID,   occurName,   involvedUID, involvedName, roleUID, roleName of involved object.
    pOccTable: wholeUID,   wholeName,   partUID,     partName
    """
        
        global drawings, sheet, boxes, lines, drawXScroll, drawYScroll, occTable, seqTable, ioTable, pOccTable
        global leftStrFrame, rightStrFrame, leftStrTree, rightStrTree, leftStrScroll, rightStrScroll
        global test

        self.sheetNr  = 0

    # Determine top(s) of composition hierarchy/hierarchies
        topUIDs  = []
        topNames = []
        nrOfTops = 0
        partRelList = [row[i] for row in pOccTable for i in range(2,3)]
        for row2 in pOccTable:
            if  row2[0] != partRelList and row2[1] not in topNames:        # if whole UID not in list of partUIDs, then
                nrOfTops = nrOfTops + 1     # nr of occurrences on topsheet
                topUIDs.append(row2[0])
                topNames.append(row2[1])    # wholeName is a name of a top occurrence

        if nrOfTops == 0:
            if test: print('*** No top occurrence identified')
            return
    # Draw top occurrences on one or more sheet(s)
        parentID = '0'
        sheetNr = MultipleSheets(sheetNr,parentID,nrOfTops,topUIDs,topNames)

    # Determine parts per top occurrence for drawing on sheet(s)
        DrawPartOccurrences(sheetNr,parentID,topUIDs)
        return
    #--------------------------------------------------------
    def DrawPartOccurrences(sheetNr,parentID,UIDs):
        partUIDs = []
        partNames= []
        nrOfOccs = 0
        parts = False
        seq = 0
        for topOcc in UIDs:
            seq = seq + 1
            childID = parentID + '.' + str(seq)
            for row in pOccTable:
                if  row[0] == topOcc:        # if whole UID on previous sheet, then there is a part:
                    parts = True
                    nrOfOccs = nrOfOccs + 1     # nr of occurrences on sheet
                    partUIDs.append(row[2])
                    partNames.append(row[3])    # wholeName is a name of a top occurrence
    # Draw part occurrences on sheet(s)
            if parts == True:
                sheetNr = MultipleSheets(sheetNr,childID,nrOfOccs,partUIDs,partNames)
            
        if parts == True:
            DrawPartOccurrences(sheetNr,childID,partUIDs)
        return
    #--------------------------------------------------------
    def MultipleSheets(sheetNr,parentID,totalNrOfBoxes,occUIDs,occNames):
        """Determine nr of sheets for one drawing and call DrawingOfOneSheet
    totalNrOfBoxes to be drawn on one drawing may require more than one drawing sheet."""

        maxBoxesPerSheet = 7
        firstBox = 0
        
        nrOfSheets = (totalNrOfBoxes-1)/maxBoxesPerSheet + 1
        intSheet = int(nrOfSheets)
        rest = totalNrOfBoxes - (intSheet-1)*maxBoxesPerSheet
        shText  = parentID
        if test: print('nrOfSheets, totalNrOfBoxes,rest:',intSheet,totalNrOfBoxes,occNames,rest,shText)
        for shNr in range(1,intSheet+1):
            if shNr == intSheet:
                nrBoxesPerSheet = rest
            else:
                nrBoxesPerSheet = maxBoxesPerSheet
            sheetNr = sheetNr + 1
            schema = ['Sheet-' + shText, 'Blad-' + shText]
            sheetName = schema[langGUIIndex]
            DrawingOfOneSheet(sheetNr,sheetName,nrBoxesPerSheet,occUIDs[firstBox:],occNames[firstBox:],parentID)  # Call Drawing for one sheet.
            firstBox = firstBox + maxBoxesPerSheet
            shText = shText + '-' + str(shNr)
            if test: print('Boxes on sheet:',sheetNr,occNames[firstBox:])
            if test: print('Lines on sheet:',sheetNr,lines)
        return sheetNr
    #--------------------------------------------------------

    def RightMouseButton(event):
        '''Handle left mouse button click events in occurModel (actTree).'''
        
        global scrWidth,scrHeight, occTable
        global sheet, boxW2, boxH2, viewsNoteb, sheetNr
        
        print('Activity details: x = %d, y = %d' % (event.x, event.y))  # x,y = Nr of pixels

        midPts = BoxType1(event.x,event.y)
        
        return midPts
    #-------------------------------------------------------------
    def DrawingOfOneSheet(sheetNr,sheetName,nrOfOccs,occUIDs,occNames,parentID):
        """Create a Notebook page and draw one sheet on that page by calling BoxType1
    and draw lines between them by calling CreateLine.
    - parentID: the ID of the whole occurrence (box) of which the occNames (occurrences) are parts.
    """

        global scrWidth,scrHeight, occTable, ioTable
        global sheet, boxW2, boxH2, viewsNoteb, drawings
        global boxes, boxesOnSheet, lines, linesOnSheet, drawXScroll, drawYScroll
        global occNoteb
        global leftStrFrame, rightStrFrame, leftStrTree, rightStrTree, leftStrScroll, rightStrScroll
        global test

        outputUID = 640019      # output role
        inputUID  = 640016      # input role
        actorUID  = 5036        # actor role (supertype of mechanism)
        subOutputUIDs = DetermineSubtypeList(outputUID)
        subInputUIDs  = DetermineSubtypeList(inputUID)
        subActorUIDs  = DetermineSubtypeList(actorUID)

    # Occurrences drawing Frame tab    
        drawings.append(ttk.Frame(occNoteb))
        drawings[sheetNr-1].grid(column=0,row=0,sticky=NSEW)
        drawings[sheetNr-1].columnconfigure(0,weight=1)
        drawings[sheetNr-1].columnconfigure(1,weight=1)
        drawings[sheetNr-1].rowconfigure(0,weight=1)
        drawings[sheetNr-1].config(borderwidth=5)
        #drawings[sheetNr-1].rowconfigure(1,weight=1)
        occNoteb.add(drawings[sheetNr-1], text=sheetName, sticky=NSEW)
        occNoteb.insert("end",drawings[sheetNr-1],sticky=NSEW)

        thick = 2
        #sheet = Canvas(drawing, width=scrWidth, height=scrHeight,background='#ddf')
        sheet.append(Canvas(drawings[sheetNr-1],width=scrWidth-100,height=scrHeight-200, background='#ddf')) # Canvas
        sheet[sheetNr-1].grid(column=0,row=0,columnspan=2,sticky=NSEW)
        sheet[sheetNr-1].bind('<Button-2>', RightMouseButton)
        sheet[sheetNr-1].columnconfigure(0,weight=1)
        sheet[sheetNr-1].rowconfigure(0,weight=1)
        #sheet[sheetNr-1].rowconfigure(1,weight=1)

        drawYScroll.append(ttk.Scrollbar(drawings[sheetNr-1],orient=VERTICAL,command=sheet[sheetNr-1].yview))
        drawYScroll[sheetNr-1].grid (column=2,row=0,sticky=NS+E)
        sheet[sheetNr-1].config(yscrollcommand=drawYScroll[sheetNr-1].set)
        drawXScroll.append(ttk.Scrollbar(drawings[sheetNr-1],orient=HORIZONTAL,command=sheet[sheetNr-1].xview))
        drawXScroll[sheetNr-1].grid (column=0,row=1,columnspan=2,sticky=S+EW)
        sheet[sheetNr-1].config(xscrollcommand=drawXScroll[sheetNr-1].set)

    # Stream Frames - left and right
        leftStrFrame.append(ttk.Frame(drawings[sheetNr-1]))
        leftStrFrame[sheetNr-1].columnconfigure(0,weight=1)
        leftStrFrame[sheetNr-1].rowconfigure(0,weight=0)
        leftStrFrame[sheetNr-1].rowconfigure(1,weight=1)
        leftStrFrame[sheetNr-1].grid(column=0,row=2,sticky=NSEW) #pack(fill='both',side=BOTTOM) #  #

        rightStrFrame.append(ttk.Frame(drawings[sheetNr-1]))
        rightStrFrame[sheetNr-1].columnconfigure(0,weight=1)
        rightStrFrame[sheetNr-1].rowconfigure(0,weight=0)
        rightStrFrame[sheetNr-1].rowconfigure(1,weight=1)
        rightStrFrame[sheetNr-1].grid(column=1,row=2,sticky=NSEW) #pack(fill='both',side=BOTTOM) #  #

        leftStrTree.append(ttk.Treeview(leftStrFrame[sheetNr-1],columns=('strNr','strName','strUID','strKind'),\
                                        displaycolumns     =('strNr','strName','strUID','strKind'),\
                                        selectmode='browse',height=5))

        rightStrTree.append(ttk.Treeview(rightStrFrame[sheetNr-1],columns=('strNr','strName','strUID','strKind'),\
                                         displaycolumns      =('strNr','strName','strUID','strKind'),
                                         selectmode='browse',height=5))

        sNrText = ['Number','Nummer']
        strText = ['Stream Name','Stroomnaam']
        uidText = ['UID'   ,'UID']
        kinText = ['Kind'  ,'Soort']
        leftStrTree[sheetNr-1].heading('strNr'   ,text=sNrText[langGUIIndex] ,anchor=W)
        leftStrTree[sheetNr-1].heading('strName' ,text=strText[langGUIIndex] ,anchor=W)
        leftStrTree[sheetNr-1].heading('strUID'  ,text=uidText[langGUIIndex] ,anchor=W)
        leftStrTree[sheetNr-1].heading('strKind' ,text=kinText[langGUIIndex] ,anchor=W)
        rightStrTree[sheetNr-1].heading('strNr'   ,text=sNrText[langGUIIndex] ,anchor=W)
        rightStrTree[sheetNr-1].heading('strName' ,text=strText[langGUIIndex] ,anchor=W)
        rightStrTree[sheetNr-1].heading('strUID'  ,text=uidText[langGUIIndex] ,anchor=W)
        rightStrTree[sheetNr-1].heading('strKind' ,text=kinText[langGUIIndex] ,anchor=W)
        
        leftStrTree[sheetNr-1].column('#0'       ,minwidth=10,width=10)
        leftStrTree[sheetNr-1].column('strNr'    ,minwidth=20,width=40)
        leftStrTree[sheetNr-1].column('strName'  ,minwidth=20,width=120)
        leftStrTree[sheetNr-1].column('strUID'   ,minwidth=20,width=60)
        leftStrTree[sheetNr-1].column('strKind'  ,minwidth=20,width=100)
        rightStrTree[sheetNr-1].column('#0'       ,minwidth=10,width=10)
        rightStrTree[sheetNr-1].column('strNr'    ,minwidth=20,width=40)
        rightStrTree[sheetNr-1].column('strName'  ,minwidth=20,width=120)
        rightStrTree[sheetNr-1].column('strUID'   ,minwidth=20,width=60)
        rightStrTree[sheetNr-1].column('strKind'  ,minwidth=20,width=100)

        leftStrTree[sheetNr-1].grid(column=0,row=0,sticky=NSEW)
        rightStrTree[sheetNr-1].grid(column=0,row=0,sticky=NSEW)

        leftStrTree[sheetNr-1].columnconfigure(0,weight=1)
        leftStrTree[sheetNr-1].columnconfigure(1,weight=1)
        leftStrTree[sheetNr-1].rowconfigure(0,weight=0)
        leftStrTree[sheetNr-1].rowconfigure(1,weight=1)
        rightStrTree[sheetNr-1].columnconfigure(0,weight=1)
        rightStrTree[sheetNr-1].columnconfigure(1,weight=1)
        rightStrTree[sheetNr-1].rowconfigure(0,weight=0)
        rightStrTree[sheetNr-1].rowconfigure(1,weight=1)

        leftStrTree[sheetNr-1].tag_configure('uomTag', option=None, background='#ccf')
        leftStrTree[sheetNr-1].tag_configure('occTag', option=None, background='#cfc')
        rightStrTree[sheetNr-1].tag_configure('uomTag', option=None, background='#ccf')
        rightStrTree[sheetNr-1].tag_configure('occTag', option=None, background='#cfc')

        leftStrScroll.append(ttk.Scrollbar(leftStrFrame[sheetNr-1],orient=VERTICAL,command=leftStrTree[sheetNr-1].yview))
        leftStrScroll[sheetNr-1].grid (column=0,row=0,sticky=NS+E)
        leftStrTree  [sheetNr-1].config(yscrollcommand=leftStrScroll[sheetNr-1].set)
        rightStrScroll.append(ttk.Scrollbar(drawings[sheetNr-1],orient=VERTICAL,command=rightStrTree[sheetNr-1].yview))
        rightStrScroll[sheetNr-1].grid (column=2,row=2,sticky=NS+E)
        rightStrTree  [sheetNr-1].config(yscrollcommand=rightStrScroll[sheetNr-1].set)

        centerX  = []            # X-Center of canvas
        centerY  = []            # Y-Center of canvas
        midPts   = []
        boxesOnSheet = []
        linesOnSheet = []

        boxWidth  = 100          # pixels
        boxHeight = 100          # pixels
        boxW2 = boxWidth  / 2   # 1/2Width  of boxes
        boxH2 = boxHeight / 2   # 1/2Height of boxes

        deltaX = scrWidth/(nrOfOccs+1)
        deltaY = scrHeight/(nrOfOccs+1)
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
            boxID = parentID + '.' + str(boxNr+1)

            midPts.append(BoxType1(sheet[sheetNr-1],centerX[boxNr],centerY[boxNr],occNames[boxNr],boxID))
            if test: print('NSEWPts:',boxNr,midPts[boxNr])
        boxes.append(boxesOnSheet)
        
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
        
    # ioTable: occurUID, occurName, involvedUID, involvedName, roleUID, roleName of involved object,invKindName.
    # Search for lines that have no begin/source occurrence (box), but only a destination occurrence.      
        for ioRow in ioTable:
            occUIDFrom = 0
            if ioRow[0] in occUIDs and ioRow[4] in subInputUIDs: # if inputStream to occurrence on this sheet, then
                indexTo = occUIDs.index(ioRow[0])       # indexTo is the nr of the occ that has stream as input.   
                out = False
                for row2 in ioTable:                    # if found stream is not output of any box on sheet, then
                    if ioRow[2] == row2[2] and row2[0] in occUIDs and row2[4] in subOutputUIDs:
                        out = True
                        break
                if out == False:                        # input from outside the sheet
                    streamUID  = ioRow[2]
                    streamName = ioRow[3]
                    streamKind = ioRow[6]
                    occIn  [indexTo] += 1
                    occInUp[indexTo] += 1
                    strNr = strNr + 1
                    strID = str(strNr)
                    endPt = midPts[indexTo][3]
                    beginPt = [border,midPts[indexTo][3][1]]
                    
                    x = (beginPt[0] + endPt[0])/2
                    y =  beginPt[1]
                    rhombus = RhombusPolygon(sheet[sheetNr-1],x,y,strID,rsize)
                    
                    lConnPt = rhombus[3]
                    rConnPt = rhombus[2]
                    line1Pts = [beginPt,lConnPt]
                    line2Pts = [rConnPt,endPt]
                    
                    line1 = sheet[sheetNr-1].create_line(line1Pts,fill='blue', width=thick, arrow=LAST)
                    line2 = sheet[sheetNr-1].create_line(line2Pts,fill='blue', width=thick, arrow=LAST)
                    linesOnSheet.append(line1)
                    if left == True:
                        leftStrTree[sheetNr-1].insert('',index='end',values=(strID,streamName,streamUID,streamKind),tags='occTag')
                        left = False
                    else:
                        rightStrTree[sheetNr-1].insert('',index='end',values=(strID,streamName,streamUID,streamKind),tags='occTag')
                        left = True
    # Find streams per occurrence (box) on this sheet in ioTable
    #  ioTable:   occurUID,   occurName,   involvedUID, involvedName, roleUID, roleName of involved object.
        if test: print ('subI/O-UIDs:',occUIDs,subInputUIDs,subOutputUIDs)
        for ioRow in ioTable:
            if test: print(' ioRow:',occUIDs,ioRow)
            occUIDTo = 0
            if ioRow[0] in occUIDs and ioRow[4] in subOutputUIDs:   # if outputStream from occurrence on this sheet, then
                if test: print('**outputStream:',ioRow)
                strNr = strNr + 1
                strID = str(strNr)
                occUIDFrom = ioRow[0]
                streamUID  = ioRow[2]
                streamName = ioRow[3]
                streamKind = ioRow[6]
                for row2 in ioTable:    # verify if found streamUID is input in box on sheet. If yes, then occUIDTo is known
                    if streamUID == row2[2] and row2[0] in occUIDs and row2[4] in subInputUIDs: 
                        if test: print('** inputStream:',row2)
                        occUIDTo = row2[0]          # else occUIDTo = 0
                        break
                # Determine index (in list of occUIDs) of boxFrom and boxTo 
                indexFrom = -1
                indexTo   = -1
                for index in range(0,len(occUIDs)):
                    if occUIDFrom == occUIDs[index]:
                        indexFrom = index
                    if occUIDTo == occUIDs[index]:
                        indexTo = index

                # Determine the sequenceNr of the input and output of the occurrence box and adjust Yin and Yout accordingly.            
                # Draw the stream line from box occUIDFrom to occUIDTo or to edge of sheet.
                if indexTo == -1:                   # no destination box, thus endPt is on rh side of the sheet.
                    ddyFrom   = (occOut  [indexFrom])*dy
                    ddyTo     = (occIn   [indexTo])*dy
                    if occOut[indexFrom] == 0:
                        occOutUp[indexFrom] += 1    # if not yet started downward, then middle becomes occupied.
                    occOut  [indexFrom] += 1
                    #occOut[indexTo]   += 1         # indexTo == -1
                    beginPt = [midPts[indexFrom][2][0],midPts[indexFrom][2][1] + ddyFrom] # midPts(occNr,East,x/y)
                    endPt = [scrWidth-border,beginPt[1]]
                    x = (beginPt[0] + endPt[0])/2
                    y =  beginPt[1]
                    rhombus = RhombusPolygon(sheet[sheetNr-1],x,y,strID,rsize) # rhobus on vertical line
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
                    rhombus = RhombusPolygon(sheet[sheetNr-1],x,y,strID,rsize)
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
                    rhombus = RhombusPolygon(sheet[sheetNr-1],x,y,strID,rsize)
                    uConnPt = rhombus[0]
                    lConnPt = rhombus[1]
                    line1Pts = [beginPt, mid1Pt, mid2Pt, lConnPt]
                    line2Pts = [uConnPt, mid3Pt, mid4Pt, mid5Pt,\
                                mid6Pt,  mid7Pt, mid8Pt, endPt]
                                
                    if mid5Pt[1] < 0:
                        sheet[sheetNr-1].yview_scroll(-mid5Pt[1] + 20)
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
                    rhombus = RhombusPolygon(sheet[sheetNr-1],x,y,strID,rsize)
                    uConnPt = rhombus[0]
                    lConnPt = rhombus[1]
                    line1Pts = [beginPt, mid1Pt, mid2Pt, uConnPt]
                    line2Pts = [lConnPt, mid3Pt, mid4Pt, endPt]
                if test: print('  Stream:',indexFrom,indexTo,line1Pts)
                line1 = sheet[sheetNr-1].create_line(line1Pts,fill='blue', width=thick, arrow=LAST)
                line2 = sheet[sheetNr-1].create_line(line2Pts,fill='blue', width=thick, arrow=LAST)
                linesOnSheet.append(line1)
    # Record stream in leftStrTree[sheetNr-1](s)
                if left == True:
                    leftStrTree[sheetNr-1].insert('',index='end',values=(strID,streamName,streamUID,streamKind),tags='occTag')
                    left = False
                else:
                    rightStrTree[sheetNr-1].insert('',index='end',values=(strID,streamName,streamUID,streamKind),tags='occTag')
                    left = True
                
        lines.append(linesOnSheet)
        return
    #-----------------------------------------------------------
    def BoxType1(sheet,X,Y,name,boxID):
        """Draw a box around (X,Y) = Xcenter and Ycenter
        Return midpts = N(x,y),S(x,y),E(x,y),W(x,y)
        (X,Y) = center of box on canvas"""
        
        global boxW2, boxH2 #, boxes, boxesOnSheet

        x0,y0 = X - boxW2, Y - boxH2        # TopLeft of box
        x1,y1 = X + boxW2, Y + boxH2        # BottomRight of box

        boxNr = sheet.create_rectangle(x0, y0, x1, y1, \
                               fill='#dfd', outline='black')
        boxName  = sheet.create_text(X,Y,justify=CENTER,text=name)
        boxIdent = sheet.create_text(X,Y+15,justify=CENTER,text=str(boxID))
        #boxesOnSheet.append(boxName)

        midNorth = [X        , Y - boxH2]
        midSouth = [X        , Y + boxH2]
        midEast  = [X + boxW2, Y]
        midWest  = [X - boxW2, Y]

        return midNorth,midSouth,midEast,midWest
    #-----------------------------------------------------------
    def RhombusPolygon(sheet,X,Y,strID,rsize):
        """Draw a rhombus polygon on position X,Y with its strID as text in the middle on sheet."""

        x0,y0 = X - rsize, Y             # midWest
        x1,y1 = X       , Y - rsize      # midNorth
        x2,y2 = X + rsize, Y             # midEast
        x3,y3 = X       , Y + rsize      # midSouth
        rhomNr = sheet.create_polygon(x0,y0,x1,y1,x2,y2,x3,y3,\
                             fill='#dfd', smooth=0, outline='black')
        strIdent = sheet.create_text(X,Y,justify=CENTER,text=strID)

        midNorth = [x1,y1]
        midSouth = [x3,y3]
        midEast  = [x2,y2]
        midWest  = [x0,y0]
        
        return midNorth,midSouth,midEast,midWest
    #-----------------------------------------------------------
    def exit_python(event):
        '''Exit Python when the event 'event' occurs.'''
        quit() # no arguments to quit 
        return #-----------------------------------------------------------
