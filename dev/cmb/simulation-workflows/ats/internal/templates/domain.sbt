<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>

    <!-- ATS mesh types -->
    <AttDef Type="mesh" Label="Domains" BaseType="" Abstract="true" Version="0" />

    <AttDef Type="mesh.generate-mesh" Label="Generate Mesh" BaseType="mesh">
      <ItemDefinitions>
        <Double Name="domain low coordinate" NumberOfRequiredValues="3">
          <DefaultValue>0.0</DefaultValue>
        </Double>
        <Double Name="domain high coordinate" NumberOfRequiredValues="3">
          <DefaultValue>1.0</DefaultValue>
        </Double>
        <Int Name="number of cells" NumberOfRequiredValues="3">
          <DefaultValue>1</DefaultValue>
          <RangeInfo>
            <Min Inclusive="true">1</Min>
          </RangeInfo>
        </Int>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="mesh.resource" Label="Mesh File (Resource)" BaseType="mesh" BaseName="mesh-resource">
      <ItemDefinitions>
        <Resource Name="resource">
          <Accepts>
            <Resource Name="smtk::model::Resource" />
          </Accepts>
        </Resource>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="mesh.surface" Label="Surface" BaseType="mesh">
      <AssociationsDef Name="associations" Extensible="true" NumberOfRequiredValues="1">
        <Accepts>
          <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region.labeled.surface']"></Resource>
        </Accepts>
      </AssociationsDef>
      <BriefDescription>A set of regions containing surface faces.
All regions must be from the same source mesh.</BriefDescription>
      <ItemDefinitions>
        <Void Name="verify mesh" Label="verify the mesh" Optional="true" IsEnabledByDefault="false">
          <BriefDescription>Perform a mesh audit</BriefDescription>
        </Void>
        <File Name="export mesh to file" Optional="true" IsEnabledByDefault="false">
        </File>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="mesh.subgrid" Label="TODO Subgrid" BaseType="mesh">
      <ItemDefinitions>
        <String Name="entity kind">
          <DiscreteInfo DefaultIndex="0">
            <Value Enum="cell">cell</Value>
            <Value Enum="face">face</Value>
            <Value Enum="node">node</Value>
          </DiscreteInfo>
        </String>
        <String Name="parent domain">
          <!-- TODO: what even is this? should it be pointing to something else? -->
          <DefaultValue>domain</DefaultValue>
        </String>
        <Void Name="flyweight mesh" Label="flyweight mesh" Optional="true" IsEnabledByDefault="false">
          <BriefDescription>NOT YET SUPPORTED. Allows a single mesh instead of one per entity.</BriefDescription>
        </Void>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="mesh.column" Label="TODO column" BaseType="mesh">
      <ItemDefinitions>
        <Void Name="deformable mesh" Label="deformable mesh" Optional="true" IsEnabledByDefault="false">
          <BriefDescription>Will this mesh be deformed?</BriefDescription>
        </Void>
        <!-- “partitioner” [string] (zoltan_rcb) Method to partition the mesh. -->
        <String Name="partitioner" Optional="true">
          <DiscreteInfo DefaultIndex="0">
            <Value Enum="zoltan_rcb/map view">zoltan_rcb</Value>
            <Value Enum="METIS">metis</Value>
            <Value Enum="Zoltan">zoltan</Value>
          </DiscreteInfo>
        </String>
      </ItemDefinitions>
    </AttDef>

  </Definitions>
</SMTK_AttributeResource>
