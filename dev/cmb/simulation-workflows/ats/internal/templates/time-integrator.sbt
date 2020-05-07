<!-- These time integrators are used by PKs. Once a user makes one, they must be selected from within a PK or they will not be used -->
<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>
    <!-- Base class for all time integrators -->
    <AttDef Type="time-integrator-base" BaseType="" Abstract="true" Version="0">
    </AttDef>


    <AttDef Type="time-integrator-backward-euler" Label="Backward Euler" BaseType="time-integrator-base" Version="0">
      <ItemDefinitions>
        <!-- TODO: verbose object -->
        <!-- TODO: residual debugger -->
        <!--  -->

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

        <!-- TODO: BDF1 slover interface -->
        <!-- TODO: solver spec -->
        <!-- TODO: timestep controller -->



      </ItemDefinitions>
    </AttDef>




  </Definitions>
</SMTK_AttributeResource>
