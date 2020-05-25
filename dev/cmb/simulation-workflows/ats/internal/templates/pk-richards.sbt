<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>
    <AttDef Type="pk-richards" Label="Richards PK" BaseType="pk-physical-bdf" Version="0">
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




    <AttDef Type="pk-richards-flow" Label="Richards Flow PK" BaseType="pk-physical-bdf" Version="0">
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


  </Definitions>
</SMTK_AttributeResource>
