<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>
    <AttDef Type="checkpoint driver" BaseType="" Version="0">
      <ItemDefinitions>
        <!-- TODO: file name "checkpoint" -->
        <!-- TODO: how to set a default value? -->
        <File Name="file name base" ShouldExist="false"></File>
        <Int Name="file name digits" DefaultValue="5">
          <RangeInfo>
            <Min Inclusive="true">0</Min>
          </RangeInfo>
        </Int>
        <!-- TODO: add IOEvent spec -->
    </ItemDefinitions>
    </AttDef>
  </Definitions>
</SMTK_AttributeResource>
