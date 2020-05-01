<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>

    <!-- Region subdomains -->
    <!-- TODO: can we ensure that a user never repeats a region name? -->
    <AttDef Type="region" Label="Region" Abstract="true" Version="0"></AttDef>
    <AttDef Type="region: all" BaseType="region"></AttDef>
    <AttDef Type="region: box" BaseType="region">
      <ItemDefinitions>
        <Double Name="low coordinate" NumberOfRequiredValues="3"></Double>
        <Double Name="high coordinate" NumberOfRequiredValues="3"></Double>
      </ItemDefinitions>
    </AttDef>
    <AttDef Type="region: plane" BaseType="region">
      <ItemDefinitions>
        <Double Name="point" NumberOfRequiredValues="3"></Double>
        <Double Name="normal" NumberOfRequiredValues="3"></Double>
      </ItemDefinitions>
    </AttDef>
    <AttDef Type="region: labeled set" BaseType="region">
      <ItemDefinitions>
        <String Name="label"></String>
        <!-- TODO: the spec says that this is the same mesh file as the section above. How do we link the two? Is this okay? -->
        <Component Name="file">
          <Accepts>
            <Resource Name="smtk::attribute::Resource" Filter="attribute[type='file']"></Resource>
          </Accepts>
        </Component>
        <!-- TODO: same as above but for the mesh format! -->
        <String Name="entity">
          <DiscreteInfo  DefaultIndex="0">
            <Value Enum="cell">cell</Value>
            <Value Enum="face">face</Value>
            <Value Enum="node">node</Value>
          </DiscreteInfo>
        </String>
      </ItemDefinitions>
    </AttDef>
    <AttDef Type="region: color function" BaseType="region">
      <ItemDefinitions>
        <File Name="file" ShouldExist="true"></File>
        <Int Name="value"></Int>
      </ItemDefinitions>
    </AttDef>
    <AttDef Type="region: point" BaseType="region">
      <ItemDefinitions>
        <Double Name="point" NumberOfRequiredValues="3"></Double>
      </ItemDefinitions>
    </AttDef>
    <AttDef Type="region: logical" BaseType="region">
      <ItemDefinitions>
        <String Name="operation">
          <DiscreteInfo DefaultIndex="0">
            <Value Enum="union">union</Value>
            <Value Enum="intersect">intersect</Value>
            <Value Enum="subtract">subtract</Value>
            <Value Enum="complement">complement</Value>
          </DiscreteInfo>
        </String>
        <!-- TODO: insert a list of Strings -->
      </ItemDefinitions>
    </AttDef>
    <!-- TODO: Polygon -->
    <!-- TODO: Enumerated -->
    <!-- TODO: Boundary -->
    <!-- TODO: Box Volume Fractions -->
    <!-- TODO: Line Segment -->
  </Definitions>
</SMTK_AttributeResource>
