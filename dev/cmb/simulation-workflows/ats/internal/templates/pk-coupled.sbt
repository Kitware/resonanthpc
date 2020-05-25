<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>

    <!-- Inheritence might not be right but it doesn't really matter with current templating -->
    <AttDef Type="pk-coupled-water" Label="coupled water" BaseType="pk-base" Version="0">
      <AssociationsDef Extensible="true" NumberOfRequiredValues="1" Name="PKs order">
        <Accepts>
          <Resource Name="smtk::attribute::Resource" Filter="attribute[type='pk-base-2']"></Resource>
        </Accepts>
      </AssociationsDef>
    </AttDef>


  </Definitions>
</SMTK_AttributeResource>
