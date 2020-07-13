<?xml version="1.0" encoding="utf-8" ?>
<SMTK_AttributeResource Version="3">
  <Definitions>

    <AttDef Type="mesh.base" Label="Mesh-Base" BaseType="" Abstract="true">
    </AttDef>

    <!-- ATS mesh types -->
    <AttDef Type="mesh" Label="Mesh" BaseType="mesh.base" Abstract="true">
      <ItemDefinitions>
        <Void Name="deformable mesh" Label="Deformable" Optional="true" IsEnabledByDefault="false">
          <BriefDescription>Will this mesh be deformed?</BriefDescription>
        </Void>
        <!-- TODO Is mesh partitioner required? -->
        <!-- <String Name="partitioner" Optional="true" IsEnabledByDefault="false">
          <DiscreteInfo DefaultIndex="0">
            <Value Enum="zoltan_rcb/map view">zoltan_rcb</Value>
            <Value Enum="METIS">metis</Value>
            <Value Enum="Zoltan">zoltan</Value>
          </DiscreteInfo>
        </String> -->
      </ItemDefinitions>
    </AttDef>

    <!-- Use mesh.audit base for mesh types that include "verify mesh" -->
    <AttDef Type="mesh.audit" BaseType="mesh" Abstract="true">
      <ItemDefinitions>
        <Void Name="verify mesh" Label="Verify" Optional="true" IsEnabledByDefault="false">
          <BriefDescription>Perform a mesh audit</BriefDescription>
        </Void>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="mesh.generate" Label="Generate Mesh" BaseType="mesh" BaseName="GeneratedMesh" Abstract="true">
    </AttDef>

    <AttDef Type="mesh.generate.2d" Label="Generate Mesh 2D" BaseType="mesh.generate" BaseName="GeneratedMesh">
      <ItemDefinitions>
        <Double Name="domain low coordinate" NumberOfRequiredValues="2">
          <DefaultValue>0.0</DefaultValue>
        </Double>
        <Double Name="domain high coordinate" NumberOfRequiredValues="2">
          <DefaultValue>1.0</DefaultValue>
        </Double>
        <Int Name="number of cells" NumberOfRequiredValues="2">
          <DefaultValue>1</DefaultValue>
          <RangeInfo>
            <Min Inclusive="true">1</Min>
          </RangeInfo>
        </Int>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="mesh.generate.3d" Label="Generate Mesh 3D" BaseType="mesh.generate" BaseName="GeneratedMesh">
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

    <AttDef Type="mesh.resource" Label="Mesh File (Resource)" BaseType="mesh.audit" BaseName="MeshFile">
      <ItemDefinitions>
        <!-- Should this instead be named "model" or "model-resource"? -->
        <Resource Name="resource">
          <Accepts>
            <Resource Name="smtk::model::Resource" />
          </Accepts>
        </Resource>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="mesh.surface" Label="Surface" BaseType="mesh.audit" BaseName="SurfaceMesh">
      <AssociationsDef Name="associations" Extensible="true" NumberOfRequiredValues="1">
        <Accepts>
          <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region.labeled.surface']"></Resource>
        </Accepts>
      </AssociationsDef>
      <BriefDescription>A set of regions containing surface faces.
All regions must be from the same source mesh.</BriefDescription>
      <ItemDefinitions>
        <File Name="export mesh to file" Optional="true" IsEnabledByDefault="false">
        </File>
      </ItemDefinitions>
    </AttDef>

    <AttDef Type="mesh.subgrid" Label="Subgrid" BaseType="mesh">
      <ItemDefinitions>
        <Component Name="region" Label="Region">
          <Accepts>
            <Resource Name="smtk::attribute::Resource" Filter="attribute[type='region']" />
          </Accepts>
        </Component>
        <String Name="entity kind">
          <DiscreteInfo DefaultIndex="0">
            <Value Enum="cell">cell</Value>
            <Value Enum="face">face</Value>
            <Value Enum="node">node</Value>
          </DiscreteInfo>
        </String>
<!--         <Void Name="flyweight mesh" Label="flyweight mesh" Optional="true" IsEnabledByDefault="false">
          <BriefDescription>NOT YET SUPPORTED. Allows a single mesh instead of one per entity.</BriefDescription>
        </Void> -->
      </ItemDefinitions>
    </AttDef>


    <AttDef Type="mesh.aliased" Label="Aliased" BaseType="mesh.base">
      <ItemDefinitions>
        <Component Name="alias" Label="Alias">
          <Accepts>
            <Resource Name="smtk::attribute::Resource" Filter="attribute[type='mesh']" />
          </Accepts>
        </Component>
      </ItemDefinitions>
    </AttDef>

<!--     <AttDef Type="mesh.column" Label="TODO column" BaseType="mesh">
    </AttDef> -->

  </Definitions>
</SMTK_AttributeResource>
