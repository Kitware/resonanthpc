<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <!-- ATS's top level -->
  <Includes>
    <!-- Mesh and Regions -->
    <File>templates/domain.sbt</File>
    <!-- cycle driver -->
    <File>templates/coordinator.sbt</File>
    <!-- PKs -->
    <File>templates/process-kernel.sbt</File>
    <!-- TODO: add state -->
    <File>templates/checkpoint.sbt</File>
    <File>templates/observation.sbt</File>
    <File>templates/visualization.sbt</File>
  </Includes>
  <Views>
    <View Type="Group" Title="ATS" TopLevel="true" TabPosition="North" FilterByAdvanceLevel="true" FilterByCategory="false">
      <Views>
        <View Title="Domain"/>
        <View Title="Coordinator"/>
        <View Title="Process Kernel"/>
        <View Title="Visualization"/>
        <View Title="Checkpoint"/>
        <View Title="Observation"/>
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
    <View Type="Attribute" Title="Process Kernel">
      <AttributeTypes>
        <Att Type="pk-base"/>
      </AttributeTypes>
    </View>
    <View Type="Instanced" Title="Visualization">
      <InstancedAttributes>
        <Att Type="visualization driver" Name="visualization driver"/>
      </InstancedAttributes>
    </View>
    <View Type="Instanced" Title="Checkpoint">
      <InstancedAttributes>
        <Att Type="checkpoint driver" Name="checkpoint driver"/>
      </InstancedAttributes>
    </View>
    <View Type="Attribute" Title="Observation">
      <AttributeTypes>
        <Att Type="observation-base" Name="observations"/>
      </AttributeTypes>
    </View>
  </Views>
</SMTK_AttributeResource>
