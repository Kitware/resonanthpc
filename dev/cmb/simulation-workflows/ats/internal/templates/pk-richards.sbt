<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>
    <AttDef Type="pk-richards" Label="Richards PK" BaseType="pk-physical-bdf" Version="0">
      <ItemDefinitions>
        <Component Name="domain" Optional="true" IsEnabledByDefault="false">
          <Accepts>
            <Resource Name="smtk::attribute::Resource" Filter="attribute[type='mesh']"></Resource>
          </Accepts>
        </Component>
        <!-- TODO: - priority - boundary conditions (subsurface-flow-bc-spec) -->
        <!-- permeability type-->
        <String Name="permeability type">
          <DiscreteInfo DefaultIndex="0">
            <Value>scalar</Value>
            <Value>horizontal and vertical</Value>
            <Value>diagonal tensor</Value>
            <Value>full tensor</Value>
          </DiscreteInfo>
        </String>
        <!-- TODO: - priority - water retention evaluator (wrm-evaluator-spec) -->
        <Group Name="source term" Optional="true" IsEnabledByDefault="false">
          <ItemDefinitions>
            <String Name="source key" Units="mol s^-1">
              <DefaultValue>mass_source</DefaultValue>
            </String>
            <Void Name="source term is differentiable" Optional="true" IsEnabledByDefault="true"></Void>
            <Void Name="explicit source term" Optional="true" IsEnabledByDefault="false"></Void>
          </ItemDefinitions>
        </Group>
        <!-- TODO: - priority - diffusion (pde-diffusion-spec) -->
        <!-- TODO: diffusion preconditioner (pde-diffusion-spec), optional-->
        <!-- TODO: - priority - preconditioner (preconditioner-typed-spec) -->
        <!-- TODO: linear solver (linear-solver-typed-spec), oprional -->
        <!-- surface rel perm strategy -->
        <String Name="surface rel perm strategy">
          <DiscreteInfo DefaultIndex="0">
            <Value>none</Value>
            <Value>clobber</Value>
            <Value>max</Value>
            <Value>unsaturated</Value>
          </DiscreteInfo>
        </String>
        <!-- relative permeability method-->
        <String Name="relative permeability method">
          <DiscreteInfo DefaultIndex="0">
            <Value>upwind with Darcy flux</Value>
            <Value>upwind with gravity</Value>
            <Value>cell centered</Value>
            <Value>arithmetic mean</Value>
          </DiscreteInfo>
        </String>
        <!-- modify predictor with consistent faces-->
        <Void Name="modify predictor with consistent faces" Optional="true" IsEnabledByDefault="false"></Void>
        <!-- modify predictor for flux BCs-->
        <Void Name="modify predictor for flux BCs" Optional="true" IsEnabledByDefault="false"></Void>
        <!-- modify predictor via water content-->
        <Void Name="modify predictor via water content" Optional="true" IsEnabledByDefault="false"></Void>
        <!-- max valid change in saturation in a time step [-]-->
        <Double Name="max valid change in saturation in a time step [-]">
          <DefaultValue>-1</DefaultValue>
        </Double>
        <!-- max valid change in ice saturation in a time step [-]-->
        <Double Name="max valid change in ice saturation in a time step [-]">
          <DefaultValue>-1</DefaultValue>
        </Double>
        <!-- limit correction to pressure change [Pa]-->
        <Double Name="limit correction to pressure change [Pa]">
          <DefaultValue>-1</DefaultValue>
        </Double>
        <!-- limit correction to pressure change when crossing atmospheric [Pa]-->
        <Double Name="limit correction to pressure change when crossing atmospheric [Pa]">
          <DefaultValue>-1</DefaultValue>
        </Double>


        <!--  TODO: there's a ton more but it says they aren't typically provided by user??? -->
        <!-- permeability rescaling is one of those... -->
        <Double Name="permeability rescaling">
          <DefaultValue>1e7</DefaultValue>
          <RangeInfo>
            <Min Inclusive="false">0.0</Min>
          </RangeInfo>
        </Double>
      </ItemDefinitions>
    </AttDef>
  </Definitions>
</SMTK_AttributeResource>