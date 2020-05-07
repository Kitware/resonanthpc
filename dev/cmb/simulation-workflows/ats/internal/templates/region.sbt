<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>

    <!-- Region subdomains -->
    <AttDef Type="region" Label="Region" Abstract="true" Version="0"></AttDef>
    <AttDef Type="region.physical" BaseType="region" Abstract="true" Version="0"></AttDef>

    <AttDef Type="region.all" Label="region: all" BaseType="region.physical"></AttDef>
    <AttDef Type="region.box" Label="region: box" BaseType="region.physical">
      <ItemDefinitions>
        <Double Name="low coordinate" NumberOfRequiredValues="3"></Double>
        <Double Name="high coordinate" NumberOfRequiredValues="3"></Double>
      </ItemDefinitions>
    </AttDef>
    <AttDef Type="region.plane" Label="region: plane" BaseType="region.physical">
      <ItemDefinitions>
        <Double Name="point" NumberOfRequiredValues="3"></Double>
        <Double Name="normal" NumberOfRequiredValues="3"></Double>
      </ItemDefinitions>
    </AttDef>
    <!-- For now, all labeled regions must be surface entities -->
    <AttDef Type="region.labeled.surface" Label="region: labeled set" BaseType="region.physical">
      <AssociationsDef Extensible="true" NumberOfRequiredValues="1">
        <Accepts>
          <Resource Name="smtk::model::Resource" Filter="face"></Resource>
        </Accepts>
      </AssociationsDef>
    </AttDef>
    <AttDef Type="region.color-function" Label="region: color function" BaseType="region.physical">
      <ItemDefinitions>
        <File Name="file" ShouldExist="true"></File>
        <Int Name="value"></Int>
      </ItemDefinitions>
    </AttDef>
    <AttDef Type="region.point" Label="region: point" BaseType="region.physical">
      <ItemDefinitions>
        <Double Name="point" NumberOfRequiredValues="3"></Double>
      </ItemDefinitions>
    </AttDef>
    <AttDef Type="region.logical" Label="region: logical" BaseType="region">
      <AssociationsDef Name="associations" Extensible="true" NumberOfRequiredValues="1">
        <Accepts>
          <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region.physical']"></Resource>
        </Accepts>
      </AssociationsDef>
      <ItemDefinitions>
        <String Name="operation">
          <DiscreteInfo DefaultIndex="0">
            <Value Enum="union">union</Value>
            <Value Enum="intersect">intersect</Value>
            <Value Enum="subtract">subtract</Value>
            <Value Enum="complement">complement</Value>
          </DiscreteInfo>
        </String>
      </ItemDefinitions>
    </AttDef>
    <!-- TODO: Polygon -->
    <!-- TODO: Enumerated -->
    <!-- TODO: Boundary -->
    <!-- TODO: Box Volume Fractions -->
    <!-- TODO: Line Segment -->
  </Definitions>
</SMTK_AttributeResource>
