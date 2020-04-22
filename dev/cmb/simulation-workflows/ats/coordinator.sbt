<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>
    <AttDef Type="cycle driver" BaseType="" Version="0">
      <ItemDefinitions>
        <Double Name="start time">
          <DefaultValue>0.0</DefaultValue>
        </Double>
        <String Name="start time units">
          <DiscreteInfo DefaultIndex="0">
            <Value Enum="second">s</Value>
            <Value Enum="day">d</Value>
            <Value Enum="year">yr</Value>
          </DiscreteInfo>
        </String>
        <String Name="end-spec" Label="end">
          <ChildrenDefinitions>
            <Double Name="end time"></Double>
            <String Name="end time units">
              <DiscreteInfo DefaultIndex="0">
                <Value Enum="second">s</Value>
                <Value Enum="day">d</Value>
                <Value Enum="year">yr</Value>
              </DiscreteInfo>
            </String>
            <Int Name="end cycle"></Int>
          </ChildrenDefinitions>
          <DiscreteInfo DefaultIndex="0">
            <Structure>
              <Value>time</Value>
              <Items>
                <Item>end time</Item>
                <Item>end time units</Item>
              </Items>
            </Structure>
            <Structure>
              <Value>cycle</Value>
              <Items>
                <Item>end cycle</Item>
              </Items>
            </Structure>
          </DiscreteInfo>
        </String>
        <File Name="restart from checkpoint file" Optional="true" IsEnabledByDefault="false" ShouldExist="true"></File>
        <Double Name="wallclock duration [hrs]" Optional="true" IsEnabledByDefault="false"></Double>
        <!-- Todo "required times"-->
        <Component Name="PK tree">
          <Accepts>
            <Resource Name="smtk::attribute::Resource" Filter="attribute[type='pk-base']"></Resource>
          </Accepts>
        </Component>
      </ItemDefinitions>
    </AttDef>
  </Definitions>
</SMTK_AttributeResource>
