<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>
    <AttDef Type="pk-base" BaseType="" Abstract="true" Version="0">
      <ItemDefinitions>
        <String Name="verbosity level">
          <DiscreteInfo DefaultIndex="0">
            <Value>low</Value>
            <Value>medium</Value>
            <Value>high</Value>
            <Value>extreme</Value>
          </DiscreteInfo>
        </String>
        <!-- Todo - priority - time integrators-->
      </ItemDefinitions>
    </AttDef>
    <AttDef Type="pk-physical" BaseType="pk-base" Abstract="true" Version="0">
      <ItemDefinitions>
        <!-- Todo domain (name)-->
        <String Name="primary variable key">
          <BriefDescription>Can we get a list from each PK?</BriefDescription>
        </String>
        <!-- Todo -priority - initial condition-->
        <!-- Todo max valid change-->
        <Group Name="debugger">
          <ItemDefinitions>
            <Int Name="debug cells" Extensible="true" Optional="true" IsEnabledByDefault="false"></Int>
            <Int Name="debug faces" Extensible="true" Optional="true" IsEnabledByDefault="false"></Int>
          </ItemDefinitions>
        </Group>
      </ItemDefinitions>
    </AttDef>
    <AttDef Type="pk-bdf" BaseType="pk-base" Abstract="true" Version="0">
      <ItemDefinitions>
        <!-- Todo initial time step-->
        <!-- Todo assemble preconditioner-->
        <!-- Todo time integrator-->
        <!-- Todo preconditioner-->
      </ItemDefinitions>
    </AttDef>
    <!-- Inherit from pk-physical and copy bdf items-->
    <AttDef Type="pk-physical-bdf" BaseType="pk-physical" Abstract="true" Version="0">
      <ItemDefinitions>
        <!-- Todo initial time step-->
        <!-- Todo assemble preconditioner-->
        <!-- Todo time integrator-->
        <!-- Todo preconditioner-->
      </ItemDefinitions>
    </AttDef>
  </Definitions>
</SMTK_AttributeResource>
