<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <!-- ATS's top level -->
  <Includes>
    <!-- Mesh and Regions -->
    <File>internal/templates/domain.sbt</File>
    <File>internal/templates/region.sbt</File>
    <!-- cycle driver -->
    <File>internal/templates/coordinator.sbt</File>
    <!-- PKs -->
    <File>internal/templates/process-kernel.sbt</File>
    <File>internal/templates/state.sbt</File>
    <File>internal/templates/checkpoint.sbt</File>
    <File>internal/templates/observation.sbt</File>
    <File>internal/templates/visualization.sbt</File>
  </Includes>
  <Views>
    <View Type="Group" Title="ATS" TopLevel="true" TabPosition="North" FilterByAdvanceLevel="true" FilterByCategory="false">
      <Views>
        <View Title="Domains"/>
        <View Title="Regions"/>
        <View Title="Coordinator"/>
        <View Title="Process Kernel"/>
        <View Title="Visualization"/>
        <View Title="Checkpoint"/>
        <View Title="Observation"/>
        <View Title="State"/>
      </Views>
    </View>
    <View Type="Attribute" Title="Domains">
      <AttributeTypes>
        <Att Type="mesh"/>
      </AttributeTypes>
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
    <View Type="Attribute" Title="Visualization">
      <AttributeTypes>
        <Att Type="visualization driver"/>
      </AttributeTypes>
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
    <View Type="Instanced" Title="State">
      <InstancedAttributes>
        <Att Type="state" Name="state"/>
      </InstancedAttributes>
    </View>
  </Views>
</SMTK_AttributeResource>
