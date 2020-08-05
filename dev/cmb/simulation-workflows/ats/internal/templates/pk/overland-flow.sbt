<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>

    <!-- Inheritence might not be right but it doesn't really matter with current templating -->
    <AttDef Type="pk-overland-flow-pressure-basis-4" Label="overland flow, pressure basis 4" BaseType="pk-physical-bdf" Version="0"></AttDef>

    <AttDef Type="pk-overland-flow-pressure-basis-3" Label="overland flow, pressure basis 3" BaseType="pk-physical-bdf" Version="0">
      <AssociationsDef NumberOfRequiredValues="1" Name="slope regions">
        <Accepts>
          <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']"></Resource>
        </Accepts>
      </AssociationsDef>
      <ItemDefinitions>

        <!-- <Component Name="initial condition"> <Accepts> <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']"></Resource> </Accepts> </Component> -->

        <Component Name="elevation evaluator">
          <Accepts>
            <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']"></Resource>
          </Accepts>
        </Component>

      </ItemDefinitions>
    </AttDef>

    <AttDef Type="pk-overland-flow-pressure-basis-rc-sh" Label="overland flow, pressure basis rc sh" BaseType="pk-physical-bdf" Version="0">
      <AssociationsDef NumberOfRequiredValues="1" Name="BC regions">
        <Accepts>
          <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']"></Resource>
        </Accepts>
      </AssociationsDef>
    </AttDef>

  </Definitions>
</SMTK_AttributeResource>
