<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>

    <!-- Base class for all PKs -->
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
        <!-- TODO: - priority - time integrators-->
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="pk-base-2" BaseType="pk-base" Abstract="true" Version="0">
      <!-- The base, non-coupler pk class. -->
      <ItemDefinitions>
        <Group Name="boundary conditions" Extensible="true" Optional="true">
          <ItemDefinitions>
            <!-- Name of the condisiton, e.g. `bottom` or `BC west` -->
            <String Name="BC name"></String>
            <Component Name="regions" Extensible="true">
              <Accepts>
                <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']"></Resource>
              </Accepts>
            </Component>
            <String Name="boundary type">
              <ChildrenDefinitions>
                <Double Name="BC value"></Double>
              </ChildrenDefinitions>
              <DiscreteInfo DefaultIndex="0">
                <Structure>
                  <!-- https://amanzi.github.io/ats/input_spec/ATSNativeSpec_dev.html#dirichlet-pressure-boundary-conditions -->
                  <Value>pressure</Value>
                  <Items>
                    <Item>BC value</Item>
                  </Items>
                </Structure>
                <Structure>
                  <!-- https://amanzi.github.io/ats/input_spec/ATSNativeSpec_dev.html#neumann-mass-flux-boundary-conditions -->
                  <Value>mass flux</Value>
                  <Items>
                    <Item>BC value</Item>
                  </Items>
                </Structure>
                <Structure>
                  <Value>seepage face pressure</Value>
                  <Items>
                    <Item>BC value</Item>
                  </Items>
                </Structure>
                <Structure>
                  <Value>seepage face head</Value>
                  <Items>
                    <Item>BC value</Item>
                  </Items>
                </Structure>
                <Structure>
                  <Value>seepage face with infiltration</Value>
                  <Items>
                    <Item>BC value</Item>
                  </Items>
                </Structure>
                <Structure>
                  <Value>head</Value>
                  <Items>
                    <Item>BC value</Item>
                  </Items>
                </Structure>
                <Structure>
                  <Value>fixed level</Value>
                  <Items>
                    <Item>BC value</Item>
                  </Items>
                </Structure>
                <Structure>
                  <Value>zero gradient</Value>
                </Structure>
                <Structure>
                  <Value>critical depth</Value>
                </Structure>
                <!-- TODO: https://amanzi.github.io/ats/input_spec/ATSNativeSpec_dev.html#dynamic-boundary-condutions -->
              </DiscreteInfo>
            </String>
          </ItemDefinitions>
        </Group>
      </ItemDefinitions>
    </AttDef>

    <!-- Base class for physical PKs -->
    <AttDef Type="pk-physical" BaseType="pk-base-2" Abstract="true" Version="0">
      <ItemDefinitions>
        <!-- TODO: domain (name): this comes from the Mesh spec -->
        <String Name="primary variable key">
          <BriefDescription>Can we get a list from each PK?</BriefDescription>
        </String>
        <!-- TODO: initial condition: this is different than the ICs for state... at least I am pretty sure... -->
        <!-- TODO: max valid change-->
        <!-- TODO: includes pk-spec -->
        <Group Name="debugger">
          <ItemDefinitions>
            <Int Name="debug cells" Extensible="true" Optional="true" IsEnabledByDefault="false"></Int>
            <Int Name="debug faces" Extensible="true" Optional="true" IsEnabledByDefault="false"></Int>
          </ItemDefinitions>
        </Group>

        <!-- only a single initial condition per PK -->
        <Group Name="initial condition" Optional="true">
          <ItemDefinitions>
            <Void Name="initialize faces from cells" Optional="true" IsEnabledByDefault="true"></Void>
            <Component Name="region">
              <Accepts>
                <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']"></Resource>
              </Accepts>
            </Component>
            <String Name="components">
              <DiscreteInfo DefaultIndex="0">
                <Value Enum="cell">cell</Value>
                <Value Enum="boundary_face">boundary_face</Value>
                <Value Enum="cell,boundary_face">cell,boundary_face</Value>
              </DiscreteInfo>
            </String>
            <String Name="variable type">
              <ChildrenDefinitions>
                <Double Name="value"></Double>
                <Group Name="tabular-data" Label="Tabular Data" Extensible="true">
                  <ItemDefinitions>
                    <Double Name="X" NumberOfRequiredValues="1"></Double>
                    <Double Name="Y" NumberOfRequiredValues="1"></Double>
                  </ItemDefinitions>
                </Group>
              </ChildrenDefinitions>
              <DiscreteInfo DefaultIndex="0">
                <Structure>
                  <Value>constant</Value>
                  <Items>
                    <Item>value</Item>
                  </Items>
                </Structure>
                <Structure>
                  <Value>function</Value>
                  <Items>
                    <Item>tabular-data</Item>
                  </Items>
                </Structure>
              </DiscreteInfo>
            </String>
          </ItemDefinitions>
        </Group>

      </ItemDefinitions>
    </AttDef>

    <!-- Base class for BDF PKs -->
    <AttDef Type="pk-bdf" BaseType="pk-base-2" Abstract="true" Version="0">
      <ItemDefinitions>
        <!-- TODO: initial time step-->
        <!-- TODO: assemble preconditioner-->
        <!-- TODO: preconditioner-->
        <!-- TODO: includes pk-spec -->
        <Component Name="time integrator" Optional="true" IsEnabledByDefault="false">
          <Accepts>
            <Resource Name="smtk::attribute::Resource" Filter="attribute[type='time integrator']"></Resource>
          </Accepts>
        </Component>
        <Component Name="preconditioner" Optional="true" IsEnabledByDefault="false">
          <Accepts>
            <Resource Name="smtk::attribute::Resource" Filter="attribute[type='preconditioner-base']"></Resource>
          </Accepts>
        </Component>
      </ItemDefinitions>
    </AttDef>

    <!-- Inherit from pk-physical and copy bdf items-->
    <AttDef Type="pk-physical-bdf" BaseType="pk-physical" Abstract="true" Version="0">
      <ItemDefinitions>
        <!-- !!!!!!!!!! -->
        <!-- Copied from `pk-bdf` because SMTK does not support dual inheritence -->
        <Component Name="time integrator" Optional="true" IsEnabledByDefault="false">
          <Accepts>
            <Resource Name="smtk::attribute::Resource" Filter="attribute[type='time integrator']"></Resource>
          </Accepts>
        </Component>
        <Component Name="preconditioner" Optional="true" IsEnabledByDefault="false">
          <Accepts>
            <Resource Name="smtk::attribute::Resource" Filter="attribute[type='preconditioner-base']"></Resource>
          </Accepts>
        </Component>
        <!-- !!!!!!!!!! -->

        <!-- TODO: conserved quantity key -->
        <!-- TODO: absolute error tolerance -->
        <!-- TODO: relative error tolerance -->
        <!-- TODO: flux error tolerance -->

        <!-- TODO: includes pk-bdf-default-specs -->
        <!-- TODO: includes pk-physical-default-spec -->
      </ItemDefinitions>
    </AttDef>
  </Definitions>
</SMTK_AttributeResource>
