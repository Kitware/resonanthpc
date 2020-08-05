<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>
    <AttDef Type="pk-richards" Label="Richards PK" BaseType="pk-physical-bdf" Version="0">
      <ItemDefinitions>
        <Component Name="domain" Optional="true" IsEnabledByDefault="false">
          <Accepts>
            <Resource Name="smtk::attribute::Resource" Filter="attribute[type='mesh.base']"></Resource>
          </Accepts>
        </Component>
        <!-- TODO: - priority - boundary conditions (subsurface-flow-bc-spec) -->
        
      </ItemDefinitions>
    </AttDef>
  </Definitions>
</SMTK_AttributeResource>
