<!-- These time integrators are used by PKs. Once a user makes one, they must be selected from within a PK or they will not be used -->
<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>
    <!-- Base class for all time integrators -->
    <AttDef Type="time-integrator-base" BaseType="" Abstract="true" Version="0">
      <ItemDefinitions>
        <!-- NOTE: called `verbose object` here not `verbosity level` like other places? -->
        <String Name="verbose object">
          <DiscreteInfo DefaultIndex="0">
            <Value>low</Value>
            <Value>medium</Value>
            <Value>high</Value>
            <Value>extreme</Value>
          </DiscreteInfo>
        </String>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="time-integrator-explicit" BaseType="time-integrator-base" Label="Explicit" Version="0">
      <ItemDefinitions>
        <String Name="RK method">
          <DiscreteInfo DefaultIndex="0">
            <Value>forward Euler</Value>
            <Value>heun euler</Value>
            <Value>midpoint</Value>
            <Value>ralston</Value>
            <Value>tvd 3rd order</Value>
            <Value>kutta 3rd order</Value>
            <Value>runge kutta 4th order</Value>
          </DiscreteInfo>
        </String>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="time-integrator-backward-euler" Label="Backward Euler" BaseType="time-integrator-base" Version="0">
      <ItemDefinitions>
        <!-- TODO: residual debugger -->
        <!-- NOTE: I am not sure if this is done right -->
        <!-- <Group Name="residual debugger"> <ItemDefinitions> <Int Name="debug cells" Extensible="true" Optional="true" IsEnabledByDefault="false"></Int> <Int Name="debug faces" Extensible="true" Optional="true" IsEnabledByDefault="false"></Int>
        </ItemDefinitions> </Group> -->

        <Int Name="max preconditioner lag iterations">
          <DefaultValue>0</DefaultValue>
        </Int>
        <Void Name="freeze preconditioner" Optional="true" IsEnabledByDefault="false"></Void>
        <Void Name="extrapolate initial guess" Optional="true" IsEnabledByDefault="true"></Void>
        <Int Name="nonlinear iteration initial guess extrapolation order">
          <DefaultValue>1</DefaultValue>
        </Int>
        <Double Name="restart tolerance relaxation factor">
          <DefaultValue>1</DefaultValue>
        </Double>
        <Double Name="restart tolerance relaxation factor damping">
          <DefaultValue>1</DefaultValue>
        </Double>

        <!-- TODO: BDF1 slover interface - this isn't documneted -->

        <!-- TODO: solver spec... linear or nonlinear? these get big -->

        <!-- TODO: timestep controller -->

      </ItemDefinitions>
    </AttDef>

  </Definitions>
</SMTK_AttributeResource>
