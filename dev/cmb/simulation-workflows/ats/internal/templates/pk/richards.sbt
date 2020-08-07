<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>
    <AttDef Type="richards flow" Label="Richards Flow" BaseType="pk-physical-bdf" Version="0">
      <!-- https://github.com/amanzi/ats/blob/master/src/pks/flow/richards_pk.cc -->
      <ItemDefinitions>

        <Group Name="water retention evaluator specs">
          <!-- TODO: should this be extensible (one for N regions?) -->
          <ItemDefinitions>
            <Component Name="region">
              <Accepts>
                <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']"></Resource>
              </Accepts>
            </Component>

            <String Name="WRM Type">
              <ChildrenDefinitions>
                <Double Name="van Genuchten alpha"></Double>
                <Double Name="residual saturation"></Double>
                <Double Name="Mualem exponent l">
                  <DefaultValue>0.5</DefaultValue>
                </Double>
                <Double Name="van Genuchten m"></Double>
                <!-- n is not used if m is given -->
                <!-- <Double Name="van Genuchten n"></Double> -->
                <Double Name="smoothing interval width [saturation]">
                  <DefaultValue>0.0</DefaultValue>
                </Double>
                <Double Name="saturation smoothing interval">
                  <DefaultValue>0.0</DefaultValue>
                </Double>
              </ChildrenDefinitions>
              <DiscreteInfo DefaultIndex="0">
                <Structure>
                  <Value>van Genuchten</Value>
                  <Items>
                    <Item>van Genuchten alpha</Item>
                    <Item>van Genuchten m</Item>
                    <Item>residual saturation</Item>
                    <Item>Mualem exponent l</Item>
                    <Item>smoothing interval width [saturation]</Item>
                    <Item>saturation smoothing interval</Item>
                  </Items>
                </Structure>
              </DiscreteInfo>
            </String>
          </ItemDefinitions>
        </Group>

        <!-- permeability type-->
        <String Name="permeability type">
          <DiscreteInfo DefaultIndex="0">
            <Value>scalar</Value>
            <Value>horizontal and vertical</Value>
            <Value>diagonal tensor</Value>
            <Value>full tensor</Value>
          </DiscreteInfo>
        </String>

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

        <!-- TODO: there's a ton more but it says they aren't typically provided by user??? -->
        <!-- permeability rescaling is one of those... -->
        <Double Name="permeability rescaling">
          <DefaultValue>1e7</DefaultValue>
          <RangeInfo>
            <Min Inclusive="false">0.0</Min>
          </RangeInfo>
        </Double>

      </ItemDefinitions>
    </AttDef>

    <!-- TODO: check that this inheritence is correct. -->
    <AttDef Type="richards steady state" Label="Richards Steady State" BaseType="richards flow" Version="0">
      <!-- https://github.com/amanzi/ats/blob/master/src/pks/flow/richards_steadystate.cc -->
      <!-- TODO: The only difference is that `"max iterations"` is set default to `10` for ``"time integrator"` -->
      <ItemDefinitions></ItemDefinitions>
    </AttDef>

  </Definitions>
</SMTK_AttributeResource>
