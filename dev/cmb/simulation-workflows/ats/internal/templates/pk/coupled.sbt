<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>

    <AttDef Type="coupled water" Label="coupled water" BaseType="pk-bdf" Version="0">
      <ItemDefinitions>
        <!-- “PKs order” [Array(string)] The use supplies the names of the coupled PKs. The order must be {subsurface_flow_pk, surface_flow_pk} (subsurface first). -->
        <Component Name="subsurface pk">
          <Accepts>
            <Resource Name="smtk::attribute::Resource" Filter="attribute[type='pk-base']"></Resource>
          </Accepts>
        </Component>
        <Component Name="surface pk">
          <Accepts>
            <Resource Name="smtk::attribute::Resource" Filter="attribute[type='pk-base']"></Resource>
          </Accepts>
        </Component>

        <String Name="subsurface domain name" Optional="true"></String>
        <String Name="surface domain name" Optional="true"></String>

        <!-- water delegate -->
        <Group Name="water delegate">
          <ItemDefinitions>
            <Void Name="modify predictor with heuristic" Optional="true" IsEnabledByDefault="false"/>
            <Void Name="modify predictor damp and cap the water spurt" Optional="true" IsEnabledByDefault="false"/>
            <!-- global water face limiter -->
            <Void Name="cap the water spurt" Optional="true" IsEnabledByDefault="false"/>
            <Void Name="damp the water spurt" Optional="true" IsEnabledByDefault="false"/>
            <Void Name="damp and cap the water spurt" Optional="true" IsEnabledByDefault="false"/>
            <Double Name="cap over atmospheric">
              <DefaultValue>100</DefaultValue>
            </Double>
          </ItemDefinitions>
        </Group>

      </ItemDefinitions>
    </AttDef>

  </Definitions>
</SMTK_AttributeResource>
