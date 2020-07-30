<SMTK_AttributeResource Version="3">
  <Definitions>
    <AttDef Type="export" BaseType="operation" Label="Export to ATS" Version="0">
      <BriefDescription>
        Write ATS input file.0
      </BriefDescription>
      <ItemDefinitions>
        <!-- <Resource Name="model" Label="Model" Optional="true" IsEnabledByDefault="false" LockType="DoNotLock" AdvanceLevel="1"> <Accepts> <Resource Name="smtk::model::Resource" /> </Accepts> </Resource> -->
        <Resource Name="attributes" Label="Attributes" LockType="DoNotLock">
          <Accepts>
            <Resource Name="smtk::attribute::Resource"/>
          </Accepts>
        </Resource>
        <File Name="output-file" Label="Output File" FileFilters="XML files (*.xml);;All files (*.*)" Version="0">
          <BriefDescription>ATS file to be generated</BriefDescription>
        </File>
      </ItemDefinitions>
    </AttDef>
  </Definitions>
  <Views>
    <View Type="Instanced" Title="Export Settings" TopLevel="true" FilterByCategory="false" FilterByAdvanceLevel="false">
      <InstancedAttributes>
        <Att Name="export" Type="export"/>
      </InstancedAttributes>
    </View>
  </Views>
</SMTK_AttributeResource>
