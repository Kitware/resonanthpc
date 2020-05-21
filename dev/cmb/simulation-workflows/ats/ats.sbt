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
    <File>internal/templates/preconditioner.sbt</File>
    <File>internal/templates/time-integrator.sbt</File>
  </Includes>
  <Views>
    <View Type="Group" Title="ATS" TopLevel="true" TabPosition="North" FilterByAdvanceLevel="true" FilterByCategory="false">
      <Views>
        <View Title="Mesh"/>
        <View Title="Region"/>
        <View Title="Coordinator"/>
        <View Title="Process Kernel Info"/>
        <View Title="Visualization"/>
        <View Title="Checkpoint"/>
        <View Title="Observation"/>
        <View Title="State"/>
      </Views>
    </View>

    <View Type="Group" Title="Mesh" Style="Tiled">
      <Views>
        <View Title="Domain" />
        <View Title="Mesh Attributes" />
      </Views>
    </View>
    <View Type="Instanced" Title="Domain">
      <InstancedAttributes>
        <Att Type="domain" Name="domain-mesh"/>
      </InstancedAttributes>
    </View>
    <View Type="Attribute" Title="Mesh Attributes">
      <AttributeTypes>
        <Att Type="mesh"/>
      </AttributeTypes>
    </View>

    <View Type="Attribute" Title="Region">
      <AttributeTypes>
        <Att Type="region"/>
      </AttributeTypes>
    </View>
    <View Type="Instanced" Title="Coordinator">
      <InstancedAttributes>
        <Att Type="cycle driver" Name="cycle driver"/>
      </InstancedAttributes>
    </View>

    <!-- Process Kernel stuff -->
    <View Type="Group" Title="Process Kernel Info" Style="Tabbed" TabPosition="North">
      <Views>
        <View Title="Process Kernel"/>
        <View Title="Preconditioners"/>
        <View Title="Time Integrators"/>
      </Views>
    </View>
    <View Type="Attribute" Title="Process Kernel">
      <AttributeTypes>
        <Att Type="pk-base"/>
      </AttributeTypes>
    </View>
    <View Type="Attribute" Title="Preconditioners">
      <AttributeTypes>
        <Att Type="preconditioner-base"/>
      </AttributeTypes>
    </View>
    <View Type="Attribute" Title="Time Integrators">
      <AttributeTypes>
        <Att Type="time-integrator-base"/>
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

    <!-- State stuff -->
    <View Type="Group" Title="State" Style="Tabbed" TabPosition="North">
      <Views>
        <View Title="field evaluators"/>
        <View Title="initial conditions"/>
      </Views>
    </View>
    <View Type="Attribute" Title="field evaluators">
      <AttributeTypes>
        <Att Type="field-evaluator-base" Name="field evaluators"/>
      </AttributeTypes>
    </View>
    <View Type="Attribute" Title="initial conditions">
      <AttributeTypes>
        <Att Type="ic-base" Name="initial conditions"/>
      </AttributeTypes>
    </View>




  </Views>
</SMTK_AttributeResource>
