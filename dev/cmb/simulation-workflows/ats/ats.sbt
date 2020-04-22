<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Includes>
    <File>domain.sbt</File>
    <File>coordinator.sbt</File>
  </Includes>
  <Views>
    <View Type="Group" Title="ATS" TopLevel="true" TabPosition="North" FilterByAdvanceLevel="true" FilterByCategory="false">
      <Views>
        <View Title="Domain"/>
        <View Title="Coordinator"></View>
      </Views>
    </View>
    <View Type="Group" Title="Domain" Style="Tiled">
      <Views>
        <View Title="Mesh"/>
        <View Title="Regions"/>
      </Views>
    </View>
    <View Type="Instanced" Title="Mesh">
      <InstancedAttributes>
        <Att Type="mesh" Name="mesh"/>
      </InstancedAttributes>
    </View>
    <View Type="Attribute" Title="Regions">
      <AttributeTypes>
        <Att Type="region"/>
      </AttributeTypes>
    </View>
    <View Type="Instanced" Title="Coordinator">
      <InstancedAttributes>
        <Att Type="cycle driver" Name="cycle driver"/>
      </InstancedAttributes>
    </View>
  </Views>
</SMTK_AttributeResource>
