<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>
    <AttDef Type="field-evaluator-base" BaseType="" Abstract="true" Version="0">
    </AttDef>


    <!-- ////////////////////////////////////////////////////////////////// -->

    <AttDef Type="richards water content" BaseType="field-evaluator-base" Version="0">
      <ItemDefinitions>
        <!-- NOTE: all options here are set as optional because none are set in demos -->
        <String Name="porosity key" Optional="true" IsEnabledByDefault="false">
          <DefaultValue>porosity</DefaultValue>
        </String>
        <String Name="molar density liquid key" Optional="true" IsEnabledByDefault="false">
          <DefaultValue>molar_density_liquid</DefaultValue>
        </String>
        <String Name="saturation liquid key" Optional="true" IsEnabledByDefault="false">
          <DefaultValue>saturation_liquid</DefaultValue>
        </String>
        <String Name="cell volume key" Optional="true" IsEnabledByDefault="false">
          <DefaultValue>cell_volume</DefaultValue>
        </String>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="capillary pressure, atmospheric gas over liquid" BaseType="field-evaluator-base" Version="0">
      <!-- Cannot find any options in docs or source -->
    </AttDef>

    <AttDef Type="viscosity" BaseType="field-evaluator-base" Version="0">
      <ItemDefinitions>
        <String Name="viscosity key">
          <DefaultValue>viscosity_liquid</DefaultValue>
        </String>
        <String Name="temperature key" Optional="true" IsEnabledByDefault="false">
          <DefaultValue>temperature</DefaultValue>
        </String>
        <!-- viscosity model parameters -->
        <Group Name="viscosity model parameters">
          <ItemDefinitions>
            <!-- As far as I can tell, there is only one? -->
            <String Name="viscosity relation type">
              <DiscreteInfo DefaultIndex="0">
                <Value Enum="liquid water">liquid water</Value>
              </DiscreteInfo>
            </String>
         </ItemDefinitions>
        </Group>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="effective_pressure" BaseType="field-evaluator-base" Version="0">
      <ItemDefinitions>
        <String Name="effective pressure key" Optional="true" IsEnabledByDefault="false">
          <DefaultValue>effective_pressure</DefaultValue>
        </String>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="multiplicative evaluator" BaseType="field-evaluator-base" Version="0">
      <ItemDefinitions>

      </ItemDefinitions>
    </AttDef>

    <AttDef Type="independent variable" BaseType="field-evaluator-base" Version="0">
      <ItemDefinitions>
        <Void Name="constant in time" Optional="true" IsEnabledByDefault="true"></Void>
        <!-- name is the name of the attribute in the list -->
        <Double Name="value"></Double>
        <String Name="components">
          <DiscreteInfo DefaultIndex="0">
            <Value Enum="cell">cell</Value>
            <Value Enum="boundary_face">boundary_face</Value>
            <Value Enum="cell,boundary_face">cell,boundary_face</Value>
          </DiscreteInfo>
        </String>
        <Component Name="region">
          <Accepts>
            <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']"></Resource>
          </Accepts>
        </Component>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="independent variable - function" BaseType="field-evaluator-base" Version="0">
      <ItemDefinitions>
        <Void Name="constant in time" Optional="true" IsEnabledByDefault="true"></Void>

        <Group Name="tabular-data" Label="Tabular Data" Extensible="true">
          <ItemDefinitions>
            <Double Name="X" NumberOfRequiredValues="1"></Double>
            <Double Name="Y" NumberOfRequiredValues="1"></Double>
          </ItemDefinitions>
        </Group>

        <String Name="components">
          <DiscreteInfo DefaultIndex="0">
            <Value Enum="cell">cell</Value>
            <Value Enum="boundary_face">boundary_face</Value>
            <Value Enum="cell,boundary_face">cell,boundary_face</Value>
          </DiscreteInfo>
        </String>
        <Component Name="region">
          <Accepts>
            <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']"></Resource>
          </Accepts>
        </Component>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="eos" BaseType="field-evaluator-base" Version="0">
      <ItemDefinitions>
        <String Name="EOS basis">
          <DiscreteInfo DefaultIndex="0">
            <Value Enum="both">both</Value>
            <Value Enum="molar">molar</Value>
          </DiscreteInfo>
        </String>
        <String Name="molar density key">
          <DefaultValue>molar_density_liquid</DefaultValue>
        </String>
        <String Name="mass density key">
          <DefaultValue>mass_density_liquid</DefaultValue>
        </String>

        <String Name="EOS type">
          <ChildrenDefinitions>
            <!-- Constant -->
            <String Name="key">
              <DefaultValue>density [kg/m^3]</DefaultValue>
            </String>
            <Double Name="value">
              <DefaultValue>1000.0</DefaultValue>
            </Double>
          </ChildrenDefinitions>
          <DiscreteInfo DefaultIndex="0">
            <Structure>
              <Value>liquid water</Value>
              <!-- TODO: should this one have options? demos do not. -->
            </Structure>
            <Structure>
              <Value>constant</Value>
              <Items>
                <Item>key</Item>
                <Item>value</Item>
              </Items>
            </Structure>
            <Structure>
              <Value>vapor in gas</Value>
              <Items>
                <Item></Item>
              </Items>
            </Structure>
          </DiscreteInfo>
        </String>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="molar fraction gas" BaseType="field-evaluator-base" Version="0">
      <ItemDefinitions>
        <String Name="molar fraction key">
          <DefaultValue>mol_frac_gas</DefaultValue>
        </String>
        <String Name="temperature key" Optional="true" IsEnabledByDefault="false">
          <DefaultValue>temperature</DefaultValue>
        </String>
        <Group Name="vapor pressure model parameters">
          <ItemDefinitions>
            <!-- As far as I can tell, there is only one? -->
            <String Name="vapor pressure model type">
              <DiscreteInfo DefaultIndex="0">
                <Value Enum="water vapor over water/ice">water vapor over water/ice</Value>
              </DiscreteInfo>
            </String>
         </ItemDefinitions>
        </Group>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="overland pressure water content" BaseType="field-evaluator-base" Version="0">
      <ItemDefinitions>
        <Double Name="molar mass" Optional="true" IsEnabledByDefault="false">
          <DefaultValue>0.0180153</DefaultValue>
        </Double>
        <!-- TODO: can we make this optional??? -->
        <!-- <Void Name="allow negative water content" Optional="true" IsEnabledByDefault="false">
        </Void> -->
        <Double Name="water content rollover" Optional="true" IsEnabledByDefault="false">
          <DefaultValue>0.0</DefaultValue>
        </Double>
        <String Name="pressure key" Optional="true" IsEnabledByDefault="false">
          <DefaultValue>pressure</DefaultValue>
        </String>
        <String Name="cell volume key" Optional="true" IsEnabledByDefault="false">
          <DefaultValue>cell_volume</DefaultValue>
        </String>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="ponded depth" BaseType="field-evaluator-base" Version="0">
      <ItemDefinitions>
        <Void Name="ponded depth bar" Optional="true" IsEnabledByDefault="false"></Void>
        <String Name="height key" Optional="true" IsEnabledByDefault="false">
          <DefaultValue>ponded_depth_bar</DefaultValue>
        </String>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="compressible porosity" BaseType="field-evaluator-base" Version="0">
      <ItemDefinitions>
        <String Name="pressure key" Optional="true" IsEnabledByDefault="false">
          <DefaultValue>pressure</DefaultValue>
        </String>
        <String Name="base porosity key" Optional="true" IsEnabledByDefault="false">
          <DefaultValue>base_porosity</DefaultValue>
        </String>
        <String Name="porosity key" Optional="true" IsEnabledByDefault="false">
          <DefaultValue>porosity</DefaultValue>
        </String>
        <Group Name="compressible porosity model parameters">
          <ItemDefinitions>
            <Component Name="region">
              <Accepts>
                <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']"></Resource>
              </Accepts>
            </Component>
            <Double Name="pore compressibility [Pa^-1]">
              <DefaultValue>1.0e-9</DefaultValue>
            </Double>
         </ItemDefinitions>
        </Group>
      </ItemDefinitions>
    </AttDef>


  </Definitions>
</SMTK_AttributeResource>
