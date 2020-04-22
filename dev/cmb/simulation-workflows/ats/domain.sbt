<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>
    <AttDef Type="mesh" Label="Mesh" BaseType="" Version="0">
      <ItemDefinitions>
        <String Name="mesh type">
          <ChildrenDefinitions>
            <Double Name="domain low coordinate" NumberOfRequiredValues="3">
              <DefaultValue>0.0</DefaultValue>
            </Double>
            <Double Name="domain high coordinate" NumberOfRequiredValues="3">
              <DefaultValue>1.0</DefaultValue>
            </Double>
            <Int Name="number of cells" NumberOfRequiredValues="3">
              <DefaultValue>1</DefaultValue>
            </Int>
          </ChildrenDefinitions>
          <DiscreteInfo DefaultIndex="0">
            <Structure>
              <Value enum="generate mesh">generate mesh</Value>
              <Items>
                <Item>domain low coordinate</Item>
                <Item>domain high coordinate</Item>
                <Item>number of cells</Item>
              </Items>
            </Structure>
          </DiscreteInfo>
        </String>
      </ItemDefinitions>
    </AttDef>
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
  </Definitions>
</SMTK_AttributeResource>
