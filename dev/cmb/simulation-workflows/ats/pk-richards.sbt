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
        <!-- Todo - priority - boundary conditions-->
        <!-- Todo permeability type-->
        <!-- Todo - priority - water retention evaluator-->
        <Group Name="source term" Optional="true" IsEnabledByDefault="false">
          <ItemDefinitions>
            <String Name="source key" Units="mol s^-1">
              <DefaultValue>mass_source</DefaultValue>
            </String>
            <Void Name="source term is differentiable" Optional="true" IsEnabledByDefault="true"></Void>
            <Void Name="explicit source term" Optional="true" IsEnabledByDefault="false"></Void>
          </ItemDefinitions>
        </Group>
        <!-- Todo - priority - diffusion-->
        <!-- Todo diffusion preconditioner-->
        <!-- Todo - priority - preconditioner-->
        <!-- Todo linear solver-->
        <String Name="surface rel perm strategy">
          <DiscreteInfo DefaultIndex="0">
            <Value>upwind with Darcy flux</Value>
            <Value>upwind with gravity</Value>
            <Value>cell centered</Value>
            <Value>arithmetic mean</Value>
          </DiscreteInfo>
        </String>
        <!-- Todo - priority - relative permeability method-->
        <!-- Todo modify predictor with consistent faces-->
        <!-- Todo modify predictor for flux BCs-->
        <!-- Todo modify predictor via water content-->
        <!-- Todo max valid change in saturation in a time step [-]-->
        <!-- Todo max valid change in ice saturation in a time step [-]-->
        <!-- Todo limit correction to pressure change [Pa]-->
        <!-- Todo limit correction to pressure change when crossing atmospheric [Pa]-->
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
