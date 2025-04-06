from logSetUp import *
from pprint import pprint
from ursina import *
from datetime import date
from datetime import datetime
import os
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.first_person_controller import FirstPersonController
import time
pieceNames = ["king", "queen", "bishop", "rook", "knight", "pawn",]
pieceBaseID = {"king": "k", "queen": "q", "bishop": "b", "rook": "r", "knight": "n", "pawn": "p",}

def verifyLogPath(): #Could be changed to set log path in later iterations
    curtDate = str(date.today())
    #adjPath = PATH + "/" + curtDate
    if not(("Logs") in os.listdir(".")): os.mkdir("Logs")


    if not(("TestLogs") in os.listdir("./Logs")): os.mkdir("./Logs/TestLogs")
    return("./Logs/TestLogs")
    #for folder in os.listdir(".."): 

def writeToLog(text):
    def retriveFileName():
        filePath = __file__[::-1]
        name = ""
        for let in filePath:
            if let == "\\": return(name[3:len(name)][::-1])
            name+=let
    logPath = verifyLogPath()
    time = str(datetime.now())
    formatTime = "   " + time[11:26] + " " + time[0:11]
    formatLocation = "[" + retriveFileName() + "] "
    print("LogPath", logPath)
    log = open(logPath, "a")
    log.write(formatLocation + text + formatTime)
    log.write("\n")
    log.close()
class intVec3():
        def __init__(Self, x, y, z):
             Self.x = x
             Self.y = y
             Self.z = z
             Self.gmPos = x + y + z
        #def __str__(Self):
        #     return str(Self.x)+" , " + str(Self.y) + " , " + str(Self.z)
        def compare(Self, otherVec):
                if Self.x == otherVec.x and Self.y == otherVec.y and Self.z == otherVec.z:
                        return(True)
                return(False)
        def add(Self, tupleVec):
                newVec = intVec3(Self.x+tupleVec[0],Self.y+tupleVec[1],Self.z+tupleVec[2])
                return(newVec)
        def subIntVec(Self, intVec):
                newVec = intVec3(intVec.x-Self.x, intVec.y-Self.y, intVec.z-Self.z)
                return (newVec)
        def getStr(Self):
            return(f"({Self.x},{Self.y},{Self.z})") 
def changeAlpha(model, alpha):
        model.alpha = (alpha)

class Space(Entity):
        def __init__(Self, pos, gX, gY, gZ):
            Self.wPos = pos
            Self.gmPos = intVec3(gX,gY,gZ)
            Self.checkedSpaces = {"white": [], "black": []}#Make invisible again
            Self.genModel()
            Self.occupied = None
            Self.cntrSpot = Vec3(Self.x, Self.y-50, Self.z)
            Self.possOwner = None
            Self.on_mouse_enter = lambda: changeAlpha(Self, 120)
            Self.on_mouse_exit = lambda: changeAlpha(Self, 54)
            Self.on_click = None
        @logFunctionCall
        def spaceClicked(Self):
            if Self.possOwner != None:
                    newOwner = Self.possOwner
                    print(newOwner) ##---Check how different between the queen and pawn 
                    newOwner.pieceDeselect()
                    Self.possOwner = None
                    #if Self.occupied != None: Self.occupied.destroy()#I honestly don't remember what this was supposed to do
                    if newOwner.miscGameCheck != None: newOwner.miscGameCheck(newOwner, Self)
                    newOwner.move(Self)
                    Self.occupied = newOwner
                    #print(Self.gmPos, " IS OCCUPIED BY ", Self.occupied) 
            else:
                print("no possOwner")
        def spaceSelect(Self, piece):
                #print("Space selected")
                Self.visible = True
                Self.possOwner = piece
                Self.color = color.green
                Self.alpha = (54)
                Self.collider = "box"
                Self.on_click = lambda: Self.spaceClicked()
                Self.enabled = True
                #print(Self.gmPos)
        def spaceDeselect(Self):
                #if Self.possOwner == None: exit()#I don't actually know why this is here
                Self.collider = None
                Self.on_click = None
                Self.visible = False
                #gmPos = Self.possOwner.gmPos
                Self.possOwner = None
                Self.enabled = False
        def genModel(Self):
                super().__init__(model="cube", scale=(125,100,125),position=Vec3(Self.wPos.x, Self.wPos.y, Self.wPos.z), alpha=54, visible=False )
                Self.PARENT = Self

def knightMoves(piece):
        allPossMoves = [[],[],[],[],[],[]]
        changes2 = [2, -2]
        changes1 = [1, -1]
        gmPos = piece.gmPos
        #there may be an issue here with the knight prematurley ending some moves becuase of hitting other pieces (we'll see)
        for I in changes2:
            for i in changes1:
                allPossMoves[0].append(intVec3(gmPos.x+I,gmPos.y+i,gmPos.z))
                allPossMoves[1].append(intVec3(gmPos.x+i,gmPos.y+I,gmPos.z))
                allPossMoves[2].append(intVec3(gmPos.x,gmPos.y+I,gmPos.z+i))
                allPossMoves[3].append(intVec3(gmPos.x,gmPos.y+i,gmPos.z+I))
                allPossMoves[4].append(intVec3(gmPos.x+I,gmPos.y,gmPos.z+i))
                allPossMoves[5].append(intVec3(gmPos.x+i,gmPos.y,gmPos.z+I))
        return(allPossMoves)

def bishopMoves(piece):
        allPossMoves = [[],[],[],[],[],[],[],[],[],[],[],[]]
        gmPos = piece.gmPos
        for I in range(1,8):
               allPossMoves[0].append(intVec3(gmPos.x+I,gmPos.y+I,gmPos.z+I))
               allPossMoves[1].append(intVec3(gmPos.x-I,gmPos.y+I,gmPos.z+I))
               allPossMoves[2].append(intVec3(gmPos.x+I,gmPos.y-I,gmPos.z+I))
               allPossMoves[3].append(intVec3(gmPos.x-I,gmPos.y-I,gmPos.z+I))
               allPossMoves[4].append(intVec3(gmPos.x+I,gmPos.y+I,gmPos.z-I))
               allPossMoves[5].append(intVec3(gmPos.x-I,gmPos.y+I,gmPos.z-I))
               allPossMoves[6].append(intVec3(gmPos.x+I,gmPos.y-I,gmPos.z-I))
               allPossMoves[7].append(intVec3(gmPos.x-I,gmPos.y-I,gmPos.z-I))
               
               allPossMoves[8].append(intVec3(gmPos.x+I,gmPos.y,gmPos.z+I))
               allPossMoves[9].append(intVec3(gmPos.x-I,gmPos.y,gmPos.z+I))
               allPossMoves[10].append(intVec3(gmPos.x+I,gmPos.y,gmPos.z-I))
               allPossMoves[11].append(intVec3(gmPos.x-I,gmPos.y,gmPos.z-I))
        return(allPossMoves)

def rookMoves(piece):
        gmPos = piece.gmPos
        allPossMoves = [[],[],[],[],[],[]]
        for I in range(1,8):
             allPossMoves[0].append(intVec3(gmPos.x+I,gmPos.y,gmPos.z))
             allPossMoves[1].append(intVec3(gmPos.x,gmPos.y+I,gmPos.z))
             allPossMoves[2].append(intVec3(gmPos.x,gmPos.y,gmPos.z+I))
             allPossMoves[3].append(intVec3(gmPos.x-I,gmPos.y,gmPos.z))
             allPossMoves[4].append(intVec3(gmPos.x,gmPos.y-I,gmPos.z))
             allPossMoves[5].append(intVec3(gmPos.x,gmPos.y,gmPos.z-I))
        return(allPossMoves)

def queenMoves(piece):
        gmPos = piece.gmPos
        allPossMoves = []
        for I in rookMoves(piece):
             allPossMoves.append(I)
        for I in bishopMoves(piece):
             allPossMoves.append(I)
        return(allPossMoves)

def kingMoves(piece):
        return piece.gm.rtnPossKingMoves(piece)  ##King is handeled differently for the sake of checks
             
def pawnMoves(piece):#Pawns are a bitch and have to move completley differenty in litterly every way
        highlighted = []
        debounce = 1
        if piece.team == "black": debounce = -1
        gmPos = piece.gmPos
        allPossMoves = [gmPos.add((0,0,debounce)),gmPos.add((0,1,0)), gmPos.add((0,-1,0)) ,gmPos.add((0,1,debounce)),gmPos.add((0,-1,debounce)),
                 gmPos.add((-1,0,debounce)),gmPos.add((-1,1,debounce)), gmPos.add((-1,-1,debounce)),
                 gmPos.add((1,0,debounce)), gmPos.add((1,1,debounce)), gmPos.add((1,-1,debounce))]
        for I, V in enumerate(allPossMoves):
                     possSpace = piece.gm.getSpace(V)#Need to be stored as an inVec in a list for formatting purposes
                     if possSpace != None: 
                        if I <= 2:
                            if possSpace.occupied != None: allPossMoves[I] = "-"
                        else:
                             if possSpace.occupied != None:
                                if possSpace.occupied.team == piece.team:
                                    allPossMoves[I] = "-"
                             else:
                                    allPossMoves[I] = "-"  
                     else:
                        allPossMoves[I] = "-"
        
                
        cleanAllPossMoves = []
        for I in allPossMoves:
                if I != "-":
                        cleanAllPossMoves.append([I])
        return(cleanAllPossMoves)
def selectPawnMoves(piece):#This is seperated out so that when I need to call on the pawn moves for the checking system
        highlighted = [] #I can get just the peices and use this one to ONLY select them if I need to
        allPossMoves = pawnMoves(piece)
        tblInt = 0 
        for spaceTbl in allPossMoves:
                highlighted.append([])
                space = piece.gm.getSpace(spaceTbl[0])#Again, spaces stored in lists for formatting purposes
                space.spaceSelect(piece)
                highlighted[tblInt].append(space)
        return(highlighted)

def getPawnChecks(piece):
        gmPos = piece.gmPos
        debounce = 1
        if piece.team == "black": debounce = -1
        cleanCheckedSpaces = []
        rawCheckedSpaces = [[gmPos.add((debounce,1,0))],[gmPos.add((debounce,-1,0))],
        [gmPos.add((debounce,0,-1))],[gmPos.add((debounce,1,-1))], [gmPos.add((debounce,-1,-1))],
        [gmPos.add((debounce,0,1))], [gmPos.add((debounce,1,1))], [gmPos.add((debounce,-1,1))]]
        tblInt = 0
        for I, spaceChords in enumerate(rawCheckedSpaces):
                space = piece.gm.getSpace(spaceChords[0])
                if space != None:
                        cleanCheckedSpaces.append([])
                        cleanCheckedSpaces[tblInt].append(space)
                        tblInt += 1
        return(cleanCheckedSpaces)

        
moveFuncs = {"knight": knightMoves, "bishop": bishopMoves,"rook": rookMoves, "queen": queenMoves, "pawn": pawnMoves, "king": kingMoves}
specialMoveFuncs = {"knight": None, "bishop": None,"rook": None, "queen": None, "pawn": "pawnPromotion", "king": None}

def denyKingSpaces():
        pass

def compileValidMoves(piece, selectSpaces): #When selectSpaces is on it autmatically selects each valid move
        #print("Colpilling moves for", piece.ID)#When off it simply returns the spaces themselves 
        gm = piece.gm
        allPossMoves = []
        Type = piece.Type
        gmPos = piece.gmPos
        highlighted = []
        restrictedMove = piece.restrictedMove
        count = 0        
        if len(restrictedMove) != 0: #Way to restrict pieces movement when the king is in check
                if restrictedMove[0] == -1:
                        return highlighted
                if selectSpaces:
                        for possSpace in restrictedMove:
                                possSpace[0].spaceSelect(piece)
                        return(restrictedMove)
        
        if piece.Type != "pawn":#See above comment regarding pawns and their issues ##!!!## LOOK HERE ##!!!## I want to better encorporate this into another system later
                allPossMoves = moveFuncs[piece.Type](piece)
                if piece.Type == "king" and selectSpaces: #Ensures that the king will only used the stored spaces, so it can't move into a checked space
                        for spaceLine in gm.curtKingMoves:
                                for possSpace in spaceLine:
                                        possSpace.spaceSelect(piece)
                        return gm.curtKingMoves 
                        #||Special case|moveFuncs| curtKingMoves contains any
                tblInt = 0
                for moveDirection in allPossMoves:
                        highlighted.append([])
                        #King specific move restrictinos 
                        for I in moveDirection:                                                         #Its regular move function does not
                            if type(I) != type("-"):
                                possSpace = gm.getSpace(I)
                                if possSpace != None:
                                        if possSpace.occupied != None:
                                                if possSpace.occupied.team == piece.team:
                                                        break
                                                if selectSpaces: possSpace.spaceSelect(piece)
                                                highlighted[tblInt].append(possSpace)
                                                if selectSpaces == True: break
                                        else:
                                                if selectSpaces: possSpace.spaceSelect(piece)
                                                highlighted[tblInt].append(possSpace)
                        
                        if len(highlighted[tblInt]) == 0:
                                del highlighted[tblInt]
                        else:
                                tblInt += 1
                ##############pieceNames = ["king", "queen", "bishop", "rook", "knight", "pawn",]
##############print("---------------")
                return highlighted
        else:
                if selectSpaces == True:
                    return selectPawnMoves(piece)
                else:
                   return getPawnChecks(piece)
                #return selectPawnMoves(piece) if selectSpaces else moveFuncs["pawn"](piece)
                #if selectSpaces:
                #    return selectPawnMoves(piece, True)
                #else:
                #    for spaceTbl in moveFuncs["pawn"](piece):
                #            highlighted.append(spaceTbl[0])
                #    return(highlighted)
                            
        #else:
                #for space in restricedMove:
                        #highlighted.append(space)
    
    ##--##
@logFunctionCall
class Piece(Entity):
        def __init__(Self,gm, team, Type, gmPos):
            Self.team = team
            Self.Type = Type
            Self.gm = gm #MaybeRemove
            Self.Space = None
            Self.generateID()
            Self.genModel()
            Self.selected = False
            Self.restrictedMove = []
            Self.gmPos = gmPos
            Self.possMoves = []
            Self.miscGameCheck = specialMoveFuncs[Type]
            if gmPos.x !=-1 and gmPos.y !=-1 and gmPos.z != -1:
               Self.Space = gm.spaces[gmPos.x][gmPos.y][gmPos.z]
               Self.position = Self.Space.cntrSpot
               Self.Space.occupied = Self


                
            
        def genModel(Self):
                super().__init__(model = Self.gm.models.get(Self.Type), scale=(1,1,1),shader=lit_with_shadows_shader,collider="box")
                Self.rotation_x -= 90
                Self.PARENT = Self
                if Self.team == "white":
                        Self.color = color.white
                        Self.gm.whiteTeam.append(Self)
                else:
                        Self.color = color.black
                        Self.gm.blackTeam.append(Self)
                Self.collider.color=color.white
                Self.collider.alpha=(54)
                Self.on_click = lambda: Self.pieceClicked()#print("piece clicked")
                        #Self.pieceClicked(Self, Self)
                ##return(newModel)
        @logFunctionCall
        def move(Self, newSpace):
                log.info(f"{Self.team} {Self.Type} at {Self.gmPos.getStr()} moved to {newSpace.gmPos.getStr()}")
                if newSpace.occupied != None and newSpace.occupied.team != Self.team:
                    #Where pieces are destroyed
                    destroy(newSpace.occupied)
                    newSpace.occupied = None
                #This is for the creation of entiley new units on the board midgame
                if Self.Space != None: Self.Space.occupied = None
                Self.Space = newSpace
                Self.position = newSpace.cntrSpot
                Self.gmPos = newSpace.gmPos
                Self.collider = "box"
                Self.gm.switchTurn()
        def pieceDeselect(Self):
                Self.gm.deselBtnOff()
                Self.gm.globalDselect()
                Self.collider.visible = False
                Self.selected = False
                for I in Self.possMoves:
                     for i in I:   
                        i.spaceDeselect()
                        
        def pieceSelect(Self):
               Self.gm.deselBtnOn()
               Self.gm.globalSelect(Self)
               Self.gm.globalSelected = True
               Self.collider.visible = True
               Self.selected = True
               Self.possMoves = compileValidMoves(Self, True)
        @logFunctionCall   
        def pieceClicked(Self):
           if not Self.gm.awaitingPlayerInput:
                   #print(f"Awatinig player Input {Self.gm.awaitingPlayerInput}")
                   if Self.gm.globalSelected == Self.selected:
                           if Self.selected == True:
                                Self.pieceDeselect()
                           else:
                                Self.pieceSelect()
        def generateID(Self):
            baseID = pieceBaseID[Self.Type]
            team = Self.gm.whiteTeam if Self.team == "white" else Self.gm.blackTeam
            baseID = baseID.upper() if Self.team == "white" else baseID
            pieceIndex = 0 
            for piece in team:
                    if piece.Type == Self.Type:
                            pieceIndex += 1
            pieceIndex = "" if pieceIndex == 0 else pieceIndex 
            uniqueId = baseID + str(pieceIndex)
            Self.ID = uniqueId

@logFunctionCall       
def promotePawn(piece, space, name, uiList):
    newPiece = Piece(piece.gm, piece.team, name, piece.gmPos)
    newPiece.on_click = None
    piece.gm.awaitingPlayerInput = False
    destroy(piece)
    for I in uiList:
        destroy(I)
    piece.gm.switchTurn()#Has to be done manually as the other call of this has been voided due to the waiting on player inpu
       
def pawnPromotionCheck(piece, space):
    gm = piece.gm
    spaceVec = space.gmPos
    if spaceVec.z == gm.promotionLevel[piece.team]:
            gm.awaitingPlayerInput = True
            ttlChoices = len(pieceNames)
            ttlLenth = (ttlChoices*.125)
            rollingPos = -1*((ttlLenth/2))
            uiList = []
            for name in pieceNames:
                 uiBtn = Button(scale=(.125, .125), text=name, model="quad",position=(rollingPos,-.375), on_click= lambda name=name:promotePawn(piece, space, name, uiList))
                 uiList.append(uiBtn)
                 rollingPos += .135
            #newQueen = Piece(gm, piece.team, "queen", ID, intVec3(-1,-1,-1))
            #newQueen.move(gm.getSpace(spaceVec))
            #gm.switchTurn()
specialMoveFuncs["pawn"] = lambda piece, space: pawnPromotionCheck(piece, space)

@logFunctionCall
class GameSpace():
    def __init__(Self):
        Self.size = 1000
        Self.gmStartPos = (0-(Self.size/2), 0-(Self.size/2), 0-(Self.size/2))
        Self.models = {"king": "3DAssets\OBJ\King.obj", "knight": "3DAssets\OBJ\Knight.obj", "queen": "3DAssets\OBJ\Queen.obj",
              "rook": "3DAssets\OBJ\Rook.obj", "bishop": "3DAssets\OBJ\Bishop.obj", "pawn": "3DAssets\OBJ\Pawn.obj"}
        Self.whiteTeam = []
        Self.blackTeam = []
        Self.sqrLayers = []
        Self.spaces = []
        Self.testBlockCoolDown = 0
        Self.moveFuncs = moveFuncs
        #Self = specialMoveFuncs
        Self.turn = False #True is white False is black#Turn is switched at first to get game started
        Self.globalSelected = False
        Self.selectedPiece = None
        Self.curtKingMoves = []
        Self.prevKingMoves = []
        Self.promotionLevel = {"white": 7, "black": 0} #Always determined by X positional Axis
        Self.awaitingPlayerInput = False
        Self.statusText = None
        Self.elementsLoaded = -1#The negative indicates that the board has not started to load
        Self.elementsToLoad = 32
        Self.menuParent = None
        Self.lastKnownPosition = ""
    def updateLKP(Self):
        pass
    @logFunctionCall
    def configBoard(Self, configTxt):
            cX, cY, cZ = 0,0,0
            for char in configTxt:
                    if char == "/":
                            cZ = 0 if cZ == 7 else cZ+1
                            cX = 0
                    elif char.isdigit():
                            cX = 0 if cX == 7 else cX+int(char)#cX+1#+int(char)-1
                            if cX == 8: cX = 0
                    elif char =="|":
                            cX, cY, cZ = 0, cY + 1, 0
                    elif char == "-":
                         pass   
                    else:
                        revPieceIDs = dict(zip(pieceBaseID.values(), pieceBaseID.keys()))#Stole this line from the internet
                        team = "white" if char.upper() == char else "black"
                        kind = revPieceIDs[char.lower()]
                        #print(team + " " + kind + " made at " + str(cX) + str(cY) + str(cZ))
                        testPiece = Piece(Self, team, kind,intVec3(cX,cY,cZ))
                        #print(testPiece.world_rotation)
                        if kind == "knight": testPiece.world_rotation = Vec3(-90, 0, 90) if testPiece.gmPos.x >=4 else Vec3(-90, 0, -90)
                        cX = 0 if cX == 7 else cX + 1
                        #print(f"Loaded {Self.elementsLoaded+1} of {Self.elementsToLoad} Game Elements")
                        Self.elementsLoaded += 1
                        if Self.menuParent != None:
                                invoke(Self.menuParent.updateLoadingScreen)
            #writeToLog("Board Loaded Successfully")
                    #print(cX, cY, cZ)  
    @logFunctionCall                    
    def checkMate(Self, teamInCheck): ##Continue this script later
            if len(Self.curtKingMoves) == 0:      
                canSaveKing = 0
                for piece in teamInCheck:
                    if piece.Type != "king" and piece.restrictedMove != [-1]:
                            canSaveKing += 1
                if canSaveKing == 0:
                        print("CHECKMATE: ", piece.team, " LOSES!")
                        Self.statusText = Text(text="YOU ARE IN CHECK", origin=(.5, .2), color=color.red,size=(10,10))
                        Self.awaitingPlayerInput = True#A cheap hack, will prevent the player from making any more moves
                        return True
                else:
                        return False
                                            
    def findKingAndSpaces(Self, team):
        for bP in team: #Could at some point create a special king variable to be put into the gameSpace class
            if bP.Type == "king":
                Self.curtKingMoves = compileValidMoves(bP, False)
                return bP
    def dispKingInCheck(Self):
            Self.statusText = Text(text="YOU ARE IN CHECK", origin=(.5, .2), color=color.red,size=(10,10))
            #Entity(model="quad", origin=txt.origin, color=color.gray,size=txt.size*2)
            
    def restrictMoves(Self, curtTurn, checkedThrough, enemyPiece, kingInCheck, king):
        #del checkedThrough[(len(checkedThrough) -1)]
        
        checkedThrough.insert(0, enemyPiece.Space)
        #print(len(checkedThrough))
        #for space in checkedThrough:
       #     #space.enabled = True
       #     space.color = color.yellow
       #     space.visible = True
       #     print(space.gmPos.getStr())
        if kingInCheck == True and enemyPiece.Type != "pawn" and enemyPiece.Type != "knight": #This is all to prevent the king from moving into a space it can't
                lastSpace = checkedThrough[len(checkedThrough)-1].gmPos
                secondToLastSpace = checkedThrough[len(checkedThrough)-2].gmPos if len(checkedThrough) != 1 else  king.gmPos
                diff = secondToLastSpace.subIntVec(lastSpace)
                if len(checkedThrough) == 1: diff = intVec3(diff.x*-1, diff.y*-1, diff.z*-1)
                newSpaceVec = king.gmPos.add((diff.x, diff.y, diff.z))
                newSpace = Self.getSpace(newSpaceVec)
                if [newSpace] in Self.curtKingMoves:
                        Self.curtKingMoves.remove([newSpace])
                                
                #if newSpace != None and newSpace in Self.curtKingMoves: Self.curtKingMoves.remove(newSpace)
                #if newSpace in Self.curtKingMoves:
                
                        
        for piece in curtTurn:
             if piece.Type != "king":
                restrictedMove = []
                moves = compileValidMoves(piece, False)
                for space in checkedThrough:
                    for moveLine in moves:
                        if space in moveLine:
                            restrictedMove.append([space])
                         #print("RestrictedMovedetected by:, ", piece.Type)
                if kingInCheck and len(restrictedMove) == 0:
                    restrictedMove = [-1]
                piece.restrictedMove = restrictedMove
                #print(restrictedMove)
        
    
    def switchTurnActions(Self, curtTurn, tookTurn):# #1 is who's turn it is, #2 is who just took their turn
        friendlyKing = Self.findKingAndSpaces(curtTurn)#This is the reason a friendly king is REQUIRED
        #print("Friedly king of who's turn it now is", friendlyKing.gmPos.print())
        # print(friendlyKing.gmPos.x, friendlyKing.gmPos.y, friendlyKing.gmPos.z)
        #print("Running for: ", tookTurn)
        for wP in tookTurn:
                raise("Test break of flow")
                wP.on_click = None #This is due to a weird quirk in the way that curtKingMoves is specific to whoevr's turn it is
                wP.restrictedMove = []
                enemyMoves = compileValidMoves(wP, False)#c #if wP.type == "king" else compileValidMoves(wP,False)
                if wP.Type == "pawn": # I tried to encorporate this part into compile Valid, moves, for formatting issues, shit just don't work
                     enemyMoves =  getPawnChecks(wP)
                     #print(enemyMoves)
                #if wP.Type == "rook":
                #        for move in enemyMoves:
                #                print(move[0].getStr())
                potPinnedPieces = 0
                pinnedPiece = None
                for moveLine in enemyMoves:
                        #if friendlyKing.gmPos in moveLine: print("King is in check")
                        checkedThrough = []
                        for space in moveLine:
                                #space = Self.getSpace(spaceChords)
                                if space != None:

                                        if [space] in Self.curtKingMoves:
                                            Self.curtKingMoves.remove([space])
                                        if space.gmPos.compare(friendlyKing.gmPos) == True:
                                                if potPinnedPieces == 0:
                                                    Self.dispKingInCheck()
                                                    Self.restrictMoves(curtTurn,checkedThrough, wP, True, friendlyKing)
                                                    Self.checkMate(curtTurn)
                                                    break
                                                else:
                                                    Self.restrictMoves(curtTurn,checkedThrough, wP, False, friendlyKing)
                                                    break
                                                
                                        if space.occupied != None:
                                            if space.occupied.team == friendlyKing.team:
                                                potPinnedPieces += 1
                                                pinnedPiece = space.occupied
                                                #continue
                                            else:
                                                break
                                checkedThrough.append(space)
                                        
        for bP in curtTurn:             
           bP.on_click = lambda bP=bP: bP.pieceClicked()
    @logFunctionCall
    def switchTurn(Self):
        if not Self.awaitingPlayerInput:
                Self.globalSelected = False
                Self.prevKingMoves = Self.curtKingMoves
                Self.curtKingMoves = []
                if Self.statusText != None:
                        destroy(Self.statusText)
                        Self.statusText = None
                if Self.turn == True:
                        #black, white
                        Self.turn = False
                        Self.switchTurnActions(Self.blackTeam, Self.whiteTeam)
                else:
                        Self.turn = True
                        Self.switchTurnActions(Self.whiteTeam, Self.blackTeam)
                
    @logFunctionCall
    def boardSetUp(Self):
        for I in range(8):
            pos = Vec3(0, (100*I)-400, 0)
            e = Entity(model=Grid(8,8), mode="line", thickness = 100, scale = (1000,1000,1000), position = pos)
            e.rotation_x += 90
            Self.sqrLayers.append(e)
        btmLeftStartPos = Vec3(Self.gmStartPos[0]+62.5, Self.gmStartPos[1]+150, Self.gmStartPos[2]+62.5)
        xChange = Vec3(btmLeftStartPos.x, btmLeftStartPos.y, btmLeftStartPos.z)
        for I in range(8):
                yChange = Vec3(xChange.x, xChange.y, xChange.z)
                Self.spaces.append([])
                for i in range(8):
                        zChange = Vec3(yChange.x, yChange.y, yChange.z)
                        Self.spaces[I].append([])
                        for j in range(8):
                             Self.spaces[I][i].append(Space(zChange, I, i, j))
                             zChange.z +=125
                        yChange.y+=100
                xChange.x+=125
    def uiSetUp(Self):
            Self.deselBtn = Text(text="Press U to Deselect", x=.5, y=.5, visible=False)
            Self.editorCamera = EditorCamera(enabled = False, position = Vec3(0,0,0), move_speed=0)
            Self.fPC = FirstPersonController(gravity = 0, speed = 0, grounded = False)
    def deselBtnOn(Self):
            Self.deselBtn.visible = True
    def deselBtnOff(Self):
            Self.deselBtn.visible = False
    def globalSelect(Self, piece):
            Self.globalSelected = True
            Self.selectedPiece = piece
    def globalDselect(Self):
            Self.globalSelected = False
            Self.selectedPiece = None
    
    def getSpace(Self, pos):#Weird bug where - numbers wrap around
        if pos.x > -1 and pos.y > -1 and pos.z > -1:
                try:
                   return Self.spaces[pos.x][pos.y][pos.z]
                except:
                   pass
        return None
    def rtnPossKingMoves(Self, king):
        allPossMoves = []
        levels = [-1,0,1]
        for Y in levels:
                for X in levels:
                        for Z in levels:
                                if Y==0:
                                   if X==0:
                                      if Z ==0: continue
                                allPossMoves.append([king.gmPos.add((X, Y, Z))])
        #print("allPossMoves", allPossMoves)
        return(allPossMoves)

class testBox(Entity):
        def __init__(Self, space, gm):
           super().__init__(model="cube")
           Self.scale = (125,100,125)
           Self.position=space.position
           Self.color = color.blue
           Self.gmPos = space.gmPos
           Self.gm = gm

        def move(Self, moveBy):
          pos = Self.gmPos
          nSC = intVec3(pos.x+moveBy.x, pos.y+moveBy.y, pos.z+moveBy.z)#newSpaceChords
          newSpace = Self.gm.getSpace(nSC)
          if newSpace != None:
             Self.position = newSpace.position
             Self.gmPos = newSpace.gmPos
class debugTools():
        def __init__(Self):
          Self.posTxt = Text(text="Vec3(0,0,0)", x=-.85, y=.5, scale=1.25)
          Self.occuTxt = Text(text="N/A", x=-.85, y=.47, scale=1.1) #Occupied
          Self.posOwnTxt = Text(text="N/A", x=-.85, y=.44, scale=1.1) #PossOwner
          Self.selected = Text(text="N/A", x=-.85, y=.41, scale=1.1) #CheckedSpaces

class uiBackgroundBox(): 
    def __init__(Self, posX, posY, sclX, sclY, a):
        Self.pos = Vec2(posX, posY) #Justified by corner
        Self.e = Entity(model="quad", position = Vec2(posX,posY), scale=(sclX,sclY), parent=camera.ui, color=color.gray, alpha=(a))
class CheckBox():
      def __init__(Self, posX, posY, scl, Func):
            Self.modelOuter = Button(position = Vec2(posX+(scl/2), posY-(scl/2)), model = "quad", color = color.black, scale = (scl,scl,scl)
                                      ,parent = camera.ui, alpha = (57),on_click=Self.changeState)
            Self.modelInner = Button(position = Vec2(posX+(scl/2), posY-(scl/2)),model = "quad", color = color.red, scale = (scl*.7,scl*.7,scl*.7)
                                      ,parent = camera.ui, alpha = (57))
            Self.extFunc = Func
            Self.state = False
      def changeState(Self):
          if Self.extFunc != None: Self.extFunc()
          if Self.state == True:
              Self.state = False
              Self.modelInner.color = color.green
          else:
             Self.state = True
             Self.modelInner.color = color.red
             
class layerButton():
    def __init__(Self,name, ID, posX, posY, sclX, sclY):
        Self.name = name
        Self.ID = ID
        Self.pos = Vec2(posX, posY)
        Self.bg = Entity(model="quad", position = Vec2(posX+(sclX/2),posY-(sclY/2)), scale=(sclX,sclY), parent=camera.ui, color=color.gray)
        Self.checkBox = CheckBox(posX+(sclX/10), posY-(sclY/8), sclY*.75, None)
        Self.text = Text(text=name, position = Vec2(posX+(sclX/2.5), posY-(sclY/4)))
        
def moveTo(toMove, pos, speed):
    toMove.world_x += pos.x*speed
    toMove.world_y += pos.y*speed
    toMove.world_z += pos.z*speed
    
def gmUpdate(gm):
    if gm.fPC.enabled == True:
        if held_keys["w"]:
            moveTo(gm.fPC,gm.fPC.forward, 4)
        if held_keys["s"]:
            moveTo(gm.fPC,gm.fPC.back, 4)
        if held_keys["a"]:
            moveTo(gm.fPC,gm.fPC.left, 4)
        if held_keys["d"]:
            moveTo(gm.fPC,gm.fPC.right, 4)
        if held_keys["e"] or held_keys["spacebar"]:
            moveTo(gm.fPC,gm.fPC.up, 4)
        if held_keys["q"]:
            moveTo(gm.fPC,gm.fPC.down, 4)
    if gm.globalSelected:
        if held_keys["u"]:
            gm.deselBtnOff()
            gm.selectedPiece.pieceDeselect()
            gm.globalDselect
        if held_keys["l"]:
            piece = gm.selectedPiece
            gm.detectCheck(piece, (0,0,1), piece.team)
def gmInput(gm, key):
    #if key == "escape":
    #    quit()
    if key == "f up":
        if gm.fPC.enabled:
            gm.editorCamera.enabled  = True
            print(gm.editorCamera.world_position)
            gm.fPC.enabled = False
        else:
            gm.fPC.enabled  = True
            gm.editorCamera.enabled = False
            print(gm.editorCamera.world_position)
    if key in "12345678":
        layer = gm.sqrLayers[int(key)-1]
        if layer.visible == True:
            layer.visible = False
        else:
            layer.visible = True
    if key == "enter":
        print("###OUTPUT-BREAK###")
        print(editorCamera.world_position)
            
