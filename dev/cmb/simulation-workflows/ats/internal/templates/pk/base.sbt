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
        
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="pk-base-2" BaseType="pk-base" Abstract="true" Version="0">
      
      <ItemDefinitions>
        <Group Name="boundary conditions" Extensible="true" Optional="true">
          <ItemDefinitions>
            
            <String Name="BC name" />
            <Component Name="regions" Extensible="true">
              <Accepts>
                <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']" />
              </Accepts>
            </Component>
            <String Name="boundary type">
              <ChildrenDefinitions>
                <Double Name="BC value" />
              </ChildrenDefinitions>
              <DiscreteInfo DefaultIndex="0">
                <Structure>
                  
                  <Value>pressure</Value>
                  <Items>
                    <Item>BC value</Item>
                  </Items>
                </Structure>
                <Structure>
                  
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
                
              </DiscreteInfo>
            </String>
          </ItemDefinitions>
        </Group>
      </ItemDefinitions>
    </AttDef>

    
    <AttDef Type="pk-physical" BaseType="pk-base-2" Abstract="true" Version="0">
      <ItemDefinitions>
        
        <String Name="primary variable key">
          <BriefDescription>Can we get a list from each PK?</BriefDescription>
        </String>
        
        
        
        <Group Name="debugger">
          <ItemDefinitions>
            <Int Name="debug cells" Extensible="true" Optional="true" IsEnabledByDefault="false" />
            <Int Name="debug faces" Extensible="true" Optional="true" IsEnabledByDefault="false" />
          </ItemDefinitions>
        </Group>

        
        <Group Name="initial condition" Optional="true">
          <ItemDefinitions>
            <Void Name="initialize faces from cells" Optional="true" IsEnabledByDefault="true" />
            <Component Name="region">
              <Accepts>
                <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']" />
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
    
    <Double Name="value" />
    
    <Group Name="tabular-data" Label="Tabular Data" Extensible="true">
      <ItemDefinitions>
        <Double Name="X" NumberOfRequiredValues="1" />
        <Double Name="Y" NumberOfRequiredValues="1" />
      </ItemDefinitions>
    </Group>
    <Group Name="forms">
      <ItemDefinitions>
        <Void Name="linear" Optional="true" IsEnabledByDefault="true" />
        <Void Name="constant" Optional="true" IsEnabledByDefault="true" />
      </ItemDefinitions>
    </Group>
    
    <Group Name="linear-data" Label="Linear Data" Extensible="true">
      <ItemDefinitions>
        <Double Name="x0" NumberOfRequiredValues="1" />
        <Double Name="gradient" NumberOfRequiredValues="1" />
      </ItemDefinitions>
    </Group>
    <Double Name="y0" />
    
  </ChildrenDefinitions>
  <DiscreteInfo DefaultIndex="0">
    <Structure>
      <Value>constant</Value>
      <Items>
        <Item>value</Item>
      </Items>
    </Structure>
    <Structure>
      <Value>function-tabular</Value>
      <Items>
        <Item>tabular-data</Item>
        <Item>forms</Item>
      </Items>
    </Structure>
    <Structure>
      <Value>function-linear</Value>
      <Items>
        <Item>linear-data</Item>
        <Item>y0</Item>
      </Items>
    </Structure>
  </DiscreteInfo>
</String>

          </ItemDefinitions>
        </Group>

      </ItemDefinitions>
    </AttDef>

    
    <AttDef Type="pk-bdf" BaseType="pk-base-2" Abstract="true" Version="0">
      <ItemDefinitions>
        
        
        
        
        <Component Name="time integrator" Optional="true" IsEnabledByDefault="false">
          <Accepts>
            <Resource Name="smtk::attribute::Resource" Filter="attribute[type='time integrator']" />
          </Accepts>
        </Component>
        <Component Name="preconditioner" Optional="true" IsEnabledByDefault="false">
          <Accepts>
            <Resource Name="smtk::attribute::Resource" Filter="attribute[type='preconditioner-base']" />
          </Accepts>
        </Component>
      </ItemDefinitions>
    </AttDef>

    
    <AttDef Type="pk-physical-bdf" BaseType="pk-physical" Abstract="true" Version="0">
      <ItemDefinitions>
        
        
        <Component Name="time integrator" Optional="true" IsEnabledByDefault="false">
          <Accepts>
            <Resource Name="smtk::attribute::Resource" Filter="attribute[type='time integrator']" />
          </Accepts>
        </Component>
        <Component Name="preconditioner" Optional="true" IsEnabledByDefault="false">
          <Accepts>
            <Resource Name="smtk::attribute::Resource" Filter="attribute[type='preconditioner-base']" />
          </Accepts>
        </Component>
        

        
        
        
        

        
        
      </ItemDefinitions>
    </AttDef>
  </Definitions>
</SMTK_AttributeResource>