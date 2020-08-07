<AttDef Type="pk-richards-flow-2" Label="Richards Flow PK 2" BaseType="pk-physical-bdf" Version="0">
  <!-- boundary conditions -->
  <AssociationsDef NumberOfRequiredValues="1" Name="boundary conditions">
    <Accepts>
      <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']"></Resource>
    </Accepts>
  </AssociationsDef>
  <ItemDefinitions>
    <Component Name="initial condition">
      <Accepts>
        <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']"></Resource>
      </Accepts>
    </Component>

    <Component Name="water retention evaluator">
      <Accepts>
        <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']"></Resource>
      </Accepts>
    </Component>

  </ItemDefinitions>
</AttDef>

<AttDef Type="pk-richards-flow-4" Label="Richards Flow PK 4" BaseType="pk-physical-bdf" Version="0">
  <ItemDefinitions>
    <Component Name="initial condition">
      <Accepts>
        <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']"></Resource>
      </Accepts>
    </Component>

    <Component Name="water retention evaluator">
      <Accepts>
        <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']"></Resource>
      </Accepts>
    </Component>

  </ItemDefinitions>
</AttDef>

<AttDef Type="pk-richards-flow-rc-sh" Label="Richards Flow PK rc sh" BaseType="pk-richards-flow-4" Version="0"></AttDef>
