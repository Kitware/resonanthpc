<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <!-- TODO: implement others as needed -->
  <!-- https://amanzi.github.io/ats/input_spec/ATSNativeSpec_dev.html#linear-solvers -->
  <Definitions>
    <AttDef Type="linear-solver-base" BaseType="" Abstract="true" Version="0"></AttDef>

    <AttDef Type="gmres" BaseType="linear-solver-base" Version="0">
      <!-- iterative method is class name -->
      <!-- parameters -->
      <ItemDefinitions>
        <Double Name="error tolerance">
          <DefaultValue>1.0e-6</DefaultValue>
        </Double>
        <Int Name="maximum number of iterations">
          <DefaultValue>100</DefaultValue>
        </Int>
        <Double Name="overflow tolerance">
          <DefaultValue>3.0e50</DefaultValue>
        </Double>
        <Int Name="size of Krylov space">
          <DefaultValue>10</DefaultValue>
        </Int>
        <Int Name="controller training start">
          <DefaultValue>0</DefaultValue>
        </Int>
        <Int Name="controller training end">
          <DefaultValue>3</DefaultValue>
        </Int>
        <Int Name="maximum size of deflation space">
          <DefaultValue>0</DefaultValue>
        </Int>
        <Group Name="convergence criteria">
          <ItemDefinitions>
            <Void Name="relative rhs" Optional="true" IsEnabledByDefault="true"/>
            <Void Name="relative residual" Optional="true" IsEnabledByDefault="false"/>
            <Void Name="absolute residual" Optional="true" IsEnabledByDefault="false"/>
            <Void Name="make one iteration" Optional="true" IsEnabledByDefault="false"/>
          </ItemDefinitions>
        </Group>
        <String Name="preconditioning strategy">
          <DiscreteInfo DefaultIndex="0">
            <Value>left</Value>
            <Value>right</Value>
          </DiscreteInfo>
        </String>
      </ItemDefinitions>
    </AttDef>

  </Definitions>
</SMTK_AttributeResource>
