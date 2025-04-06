from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.prefabs.first_person_controller import FirstPersonController
from gameSetUp import *

ttlFps = 0
numOfCounts = 0
defaultBoardSetUp = "-|-|-|RNBQKBNR/PPPPPPPP/8/8/8/8/pppppppp/rnbqkbnr|-|-|-|-"
defaultBoardSetUp = "-|-|-|1N4N1/8/8/8/8/8/8/1N4N1|-|-|-|-"


app = Ursina(borderless = False, development_mode=True)
gm = GameSpace()
gm.boardSetUp()
gm.uiSetUp()
gm.configBoard(defaultBoardSetUp)
print("Count", window.fps_counter.text)
debugTools = debugTools()
#layerButton("Layer 1", "L1", 0,0,.15,.05)
Entity(model="sphere", position = gm.gmStartPos, color = color.blue, alpha = (54), scale=(50,50,50))
#pieceNames = ["king", "queen", "bishop", "rook", "knight", "pawn",]
centerSquare = Entity(model="sphere", position = Vec3(-700,0,0), color = color.green, alpha = (54), scale=(50,50,50))
zPos = -300
#Manually Adding Pieces for debug purposes
#whiteTestPiece = Piece(gm, "white", "king",intVec3(7,0,0))
#testPiece = Piece(gm, "white", "rook",intVec3(0,6,1))
#testPiece = Piece(gm, "white", "pawn",intVec3(6,7,3))
#testPiece = Piece(gm, "white", "rook",intVec3(1,6,0))
#testPiece = Piece(gm, "white", "rook",intVec3(0,6,0))


#testPiece = Piece(gm, "black", "king",intVec3(7,7,0))
#testPiece = Piece(gm, "black", "queen",intVec3(0,0,0))
#testPiece = Piece(gm, "black", "rook",intVec3(5,6,7))
#testPiece = Piece(gm, "black", "bishop",intVec3(0,0,0))
#gm.switchTurn()

#b = 

#testUI2 = CheckBox(1, 1, 1, lambda:print("Test2"))
#testUI = promotionBox("peice")#promotionBox()

#newPiece.position = testSpace.cntrSpot
#for I in pieceNames:5
#    print(I)
#    print(zPos)
#    newPiece = Piece(gm, "white", I, "N/A")5
#    newPiece.position = Vec3(-700, 50, zPos)5
#    zPos += 100
#    
#for I in pieceNames:
#    print(I)
#    print(zPos)
#    newPiece = Piece(gm, "black", I, "N/A")
#    newPiece.position = Vec3(-700, -50, zPos)
#    zPos += 100


#########################################################

def moveTo(toMove, pos, speed):
    toMove.world_x += pos.x*speed
    toMove.world_y += pos.y*speed
    toMove.world_z += pos.z*speed
speed = .5
debugBoolVar = False
if debugTools != None: debugBox = testBox(gm.spaces[1][4][3], gm)
def update():
    #5ttlFps += int(window.fps_counter.text)
    #numOfCounts +=1
    gmUpdate(gm)
            
    if debugBox != None:
        if gm.testBlockCoolDown == 0:
            #print("Hello2")
            if held_keys["up arrow"]==1:
                debugBox.move(intVec3(0,1,0))
                gm.testBlockCoolDown = 10
            if held_keys["down arrow"]==1:
               debugBox.move(intVec3(0,-1,0))
               gm.testBlockCoolDown = 10
            if held_keys["left arrow"]==1:
               debugBox.move(intVec3(1,0,0))
               gm.testBlockCoolDown = 10
            if held_keys["right arrow"]==1:
                debugBox.move(intVec3(-1,0,0))
                gm.testBlockCoolDown = 10
            if held_keys["o"]==1:
                debugBox.move(intVec3(0,0,1))
                gm.testBlockCoolDown = 10
            if held_keys["p"]==1:
                debugBox.move(intVec3(0,0,-1))
                gm.testBlockCoolDown = 10
        else:
            gm.testBlockCoolDown = 0 if gm.testBlockCoolDown-1 < 0 else gm.testBlockCoolDown-1
            #if gm.testBlockCoolDown-1 < 0: 0 else gm.testBlockCoolDown -= 1

    if debugTools != None:
        curtSpace = gm.getSpace(debugBox.gmPos)
        listOfRest = ""
        if curtSpace.occupied != None:
            for space in curtSpace.occupied.restrictedMove:
                #print(curtSpace.occupied.restrictedMove)
                listOfRest += "|" + space.gmPos.getStr() + "|"
        debugTools.posTxt.text = "Position: " + str(debugBox.gmPos.getStr())
        debugTools.occuTxt.text = "listOfRest: " + listOfRest
        if curtSpace.collider != None:
            debugTools.posOwnTxt.text = "Collider: " + str(curtSpace.collider)
        else:
            debugTools.posOwnTxt.text = None
    #if gm.globalSelected == True:
        

def input(key):
    gmInput(gm, key)


    
app.run()


