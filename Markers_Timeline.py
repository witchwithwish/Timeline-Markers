import maya.cmds as cmds


class Markers_window():

    def __init__(self):
        
        #make a window
        self.wind = 'Marker_Win'

        if cmds.window(self.wind, exists=True):
            cmds.deleteUI(self.wind)

        cmds.window(self.wind, title='Marker Adder', widthHeight=(300, 300),sizeable=True)
        menubar_layout = cmds.menuBarLayout()
        cmds.menu(label="Option")
        cmds.menuItem(label="Delete Select Markers", command = self.clear_sel_marker)
        cmds.menuItem(label="Clear All Markers", command = self.clear_Marker)
        cmds.menuItem(divider=True)
        cmds.menuItem(label="Store Markers In Scene",command = self.storeMarkers)
        cmds.menuItem(label="Reload Scene", command = self.reloadMarkers)
        cmds.menuItem(label="Delete Markers From Scene", command = self.deleteMarkers)
        
        mainColumnLayout = cmds.columnLayout(h=300,w=300, adj=True)
        cmds.iconTextStaticLabel( st='textOnly',l="Marker" )
                
        cmds.textScrollList('marker_TSL', h=150,w=150, 
                            allowMultiSelection = False, 
                            selectCommand = self.jump_to_marker)
        	  
        
        cmds.rowColumnLayout( numberOfColumns=2 )
        text_d_field = cmds.textField('marker_field',aie=True, width=300)
        
        cmds.showWindow()
        cmds.setParent(mainColumnLayout)
        cmds.button(label='Add Marker', command= self.add_Marker)
          
        


    def add_Marker(*args):
        frameNumber = cmds.currentTime(q=True) 
        frameNumber = int(frameNumber)
        marker_name = cmds.textField('marker_field', q=True, text=True)
        marker_string = str(frameNumber) + " : " + marker_name
        cmds.textScrollList('marker_TSL', edit=True, append=marker_string)
        cmds.textField('marker_field',edit=True, text="")
    
    def clear_Marker(*args):
        cmds.textScrollList('marker_TSL', q=True, edit=True, removeAll=True)
        print("Cleared Markers from list but node still exists in scene..")

    def clear_sel_marker(*args):
        select_text = cmds.textScrollList('marker_TSL', q=True, selectItem=True)
        cmds.textScrollList('marker_TSL', edit=True, removeItem=select_text[0])


    def jump_to_marker(*args):
        mods = cmds.getModifiers()
        select  = cmds.textScrollList('marker_TSL', q=True, selectItem=True)
        frame_space = select[0].split(" : ")
        jump_frame = frame_space[0]
        go_frame = int(jump_frame)
        cmds.currentTime(jump_frame, edit=True)
        print("Jumped to marker {} on frame {}".format(frame_space[1], frame_space[0]))
            
        if mods / 4 % 2:
            cmds.playbackOptions(edit=True, min=go_frame)
            
        if mods / 8 % 2:
            cmds.playbackOptions(edit=True, max=go_frame)

    def storeMarkers(*args):
    
    # does the marker node already exist?
        if cmds.objExists('timelineMarkersNode'):
            cmds.delete('timelineMarkersNode')
    
        marker_node = cmds.spaceLocator(n='timelineMarkersNode') 
        # create the locator to store the markers on
    
    # hide the regular attrs to keep things neat
        for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']:
            cmds.setAttr('timelineMarkersNode.' + attr, keyable=True, channelBox=True, lock=False)
    
        cmds.setAttr(marker_node[0] + '.visibility', 0) # hide the locator in the view
        cmds.setAttr('timelineMarkersNode.visibility', keyable=True, channelBox=True, lock=False)
        
        cmds.select('timelineMarkersNodeShape')
        cmds.delete()
        
        cmds.select('timelineMarkersNode')
    
    # add the attributes here for each of the timeline markers 
        markers_count = cmds.textScrollList('marker_TSL', q=True, ni=True)
        markers_list = cmds.textScrollList('marker_TSL', q=True, ai=True)
    
        for marker in markers_list:
            new_marker_name = marker
            frame_space = new_marker_name.split(' : ')
            frame_nub = frame_space[0]
            frame_name = frame_space[1]
            frame_val = int(frame_nub)
            
            # add an attribute for each marker
            cmds.addAttr('timelineMarkersNode', ln=frame_name, at='double')
            cmds.setAttr('timelineMarkersNode.' + frame_name, e=True, keyable=True)
            
            # store the markers frame number in the attribute
            cmds.setAttr('timelineMarkersNode.' + frame_name, frame_val)
        
        print('Saved Timeline Markers...')

    def reloadMarkers(*args):
        cmds.textScrollList("marker_TSL", edit=True, removeAll=True)
        mrkLoc = "timelineMarkersNode"
        attrs1 = cmds.listAttr(mrkLoc, userDefined=True, keyable=True, scalar=True, unlocked=True)

        # cycle through the custom attributes and load into the text scroll list
        for ac in range(len(attrs1)):
            attrName = attrs1[ac]
            attrVal = cmds.getAttr(mrkLoc + "." + attrs1[ac])
            markerString = str(attrVal) + " : " + attrName
            cmds.textScrollList("marker_TSL", edit=True, append=markerString)

        cmds.select(mrkLoc, replace=True)
        print("Reloaded Timeline Markers...")


    def deleteMarkers(*args):
        if cmds.objExists("timelineMarkersNode"):
            cmds.delete("timelineMarkersNode")
            print("Deleted Timeline Markers Node from Scene..")
    

Markers_window()