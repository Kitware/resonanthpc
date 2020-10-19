<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>

    <AttDef Type="overland flow, pressure basis" Label="overland flow, pressure basis" BaseType="pk-physical-bdf" Version="0">
      <!-- <AssociationsDef NumberOfRequiredValues="1" Name="slope regions"> <Accepts> <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']"></Resource> </Accepts> </AssociationsDef> -->
      <ItemDefinitions>

        <!-- limit correction to pressure change [Pa] (-1) -->
        <Double Name="limit correction to pressure change [Pa]">
          <DefaultValue>-1</DefaultValue>
        </Double>
        <!-- limit correction to pressure change when crossing atmospheric [Pa] (-1) -->
        <Double Name="limit correction to pressure change when crossing atmospheric [Pa]">
          <DefaultValue>-1</DefaultValue>
        </Double>
        <!-- allow no negative ponded depths (false) -->
        <Void Name="allow no negative ponded depths" Optional="true" IsEnabledByDefault="false"></Void>
        <!-- min ponded depth for velocity calculation (1.0e-2) -->
        <Double Name="min ponded depth for velocity calculation">
          <DefaultValue>1.0e-2</DefaultValue>
        </Double>
        <!-- min ponded depth for tidal bc (0.02) -->
        <Double Name="min ponded depth for tidal bc">
          <DefaultValue>0.02</DefaultValue>
        </Double>

      </ItemDefinitions>
    </AttDef>

  </Definitions>
</SMTK_AttributeResource>
